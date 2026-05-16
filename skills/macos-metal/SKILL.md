# macOS Metal Skill

## Overview

Provides Metal rendering frameworks, GPU optimization patterns, Vision Pro integration, and spatial computing architecture for macOS and visionOS applications. Covers instanced rendering, compute shaders, Compositor Services, triple buffering, and profiling methodology for achieving 90fps stereoscopic rendering with 25k+ nodes.

## Capabilities

### Metal Rendering Pipeline Architecture

**Core Rendering Stack**
```swift
// MetalGraphRenderer — instanced node + edge rendering
class MetalGraphRenderer {
    private let device: MTLDevice
    private let commandQueue: MTLCommandQueue
    private var nodePipelineState: MTLRenderPipelineState
    private var edgePipelineState: MTLRenderPipelineState
    private var depthState: MTLDepthStencilState

    // Per-instance GPU data (keep tightly packed for cache efficiency)
    struct NodeInstance {
        var position: SIMD3<Float>   // 12 bytes
        var color: SIMD4<Float>      // 16 bytes
        var scale: Float             // 4 bytes
        var symbolId: UInt32         // 4 bytes — 36 bytes total, fits in cache line
    }

    // GPU buffers — always private storage mode for GPU-resident data
    private var nodeBuffer: MTLBuffer        // Per-instance NodeInstance array
    private var edgeBuffer: MTLBuffer        // Packed (start, end) SIMD3<Float> pairs
    private var uniformBuffer: MTLBuffer     // View/projection matrices, time
    private var semaphore: DispatchSemaphore // Triple-buffer synchronization
}
```

**Triple Buffering Pattern**
```swift
// Prevents CPU/GPU stall — never overwrite buffer the GPU is reading
private let maxInflightFrames = 3
private var currentBuffer = 0
private let frameSemaphore = DispatchSemaphore(value: 3)

func render() {
    frameSemaphore.wait()  // Block if GPU 3 frames behind
    
    defer {
        currentBuffer = (currentBuffer + 1) % maxInflightFrames
        frameSemaphore.signal()  // Release when GPU done with this frame
    }
    
    let bufferOffset = currentBuffer * alignedUniformsSize
    // Write to current buffer slot only
    uniformBuffers[currentBuffer].contents().copyMemory(from: &uniforms, byteCount: stride)
}
```

**Instanced Drawing — 10k-100k Nodes**
```swift
// One draw call for all nodes regardless of count
encoder.setRenderPipelineState(nodePipelineState)
encoder.setVertexBuffer(nodeBuffer, offset: 0, index: 0)    // Per-instance data
encoder.setVertexBuffer(uniformBuffer, offset: 0, index: 1)  // Shared uniforms
encoder.drawPrimitives(
    type: .triangleStrip,
    vertexStart: 0,
    vertexCount: 4,             // Billboard quad (2 triangles)
    instanceCount: nodes.count  // GPU handles the parallelism
)
```

**Frustum Culling — GPU Side**
```metal
// Vertex shader: discard instances outside view frustum
vertex VertexOut nodeVertex(
    uint instanceId [[instance_id]],
    device NodeInstance* instances [[buffer(0)]],
    constant Uniforms& uniforms [[buffer(1)]])
{
    NodeInstance node = instances[instanceId];
    float4 clipPos = uniforms.viewProjection * float4(node.position, 1.0);
    
    // Frustum cull: if outside clip space, collapse to degenerate triangle
    float w = clipPos.w;
    if (abs(clipPos.x) > w || abs(clipPos.y) > w || clipPos.z < 0 || clipPos.z > w) {
        VertexOut out;
        out.position = float4(2, 2, 2, 1);  // Outside NDC = clipped
        return out;
    }
    // ... normal path
}
```

### Vision Pro Compositor Services Integration

**Stereo Frame Streaming**
```swift
import CompositorServices

class VisionProCompositor {
    private var layerRenderer: LayerRenderer
    
    init() async throws {
        let config = LayerRenderer.Configuration()
        config.colorFormat = .rgba16Float
        config.depthFormat = .depth32Float
        config.layout = .dedicated  // One texture per eye (vs. layered)
        self.layerRenderer = try await LayerRenderer(configuration: config)
    }
    
    func renderLoop() async {
        for await frame in layerRenderer.frames {
            guard let drawable = try? frame.queryNextDrawable() else { continue }
            
            // Render left eye
            renderEye(drawable.leftViewport, to: drawable.colorTextures[0])
            // Render right eye  
            renderEye(drawable.rightViewport, to: drawable.colorTextures[1])
            
            frame.encodePresent(commandBuffer: commandBuffer)
            commandBuffer.commit()
        }
    }
}
```

**RemoteImmersiveSpace Setup**
```swift
// macOS companion app connecting to Vision Pro
struct ContentView: View {
    @State private var immersiveSpace = ImmersiveSpaceState.closed
    
    var body: some View {
        // ... UI
        .immersiveSpaceCapabilities([.remote])
    }
}

// Vision Pro side: receive frames from macOS
struct ImmersiveView: View {
    var body: some View {
        RealityView { content in
            // Receive rendered content via CompositorServices layer
        }
    }
}
```

### GPU-Based Force-Directed Graph Layout

**Metal Compute Shader**
```metal
kernel void updateGraphLayout(
    device Node* nodes [[buffer(0)]],
    device Edge* edges [[buffer(1)]],
    constant Params& params [[buffer(2)]],
    uint id [[thread_position_in_grid]])
{
    if (id >= params.nodeCount) return;
    float3 force = float3(0);
    Node node = nodes[id];
    
    // Repulsion: O(n²) — consider Barnes-Hut for >10k nodes
    for (uint i = 0; i < params.nodeCount; i++) {
        if (i == id) continue;
        float3 diff = node.position - nodes[i].position;
        float distSq = dot(diff, diff) + 0.1;  // Softening factor prevents division by zero
        force += normalize(diff) * (params.repulsionStrength / distSq);
    }
    
    // Attraction along edges
    for (uint i = 0; i < params.edgeCount; i++) {
        if (edges[i].source != id) continue;
        float3 diff = nodes[edges[i].target].position - node.position;
        force += normalize(diff) * (length(diff) * params.attractionStrength);
    }
    
    node.velocity = node.velocity * params.damping + force * params.deltaTime;
    node.position += node.velocity * params.deltaTime;
    nodes[id] = node;
}
```

### Spatial Interaction (Gaze + Gesture)

**GPU Raycast for Gaze Hit Testing**
```swift
class SpatialInteractionHandler {
    // Ray-sphere intersection for node selection
    func gpuRaycast(origin: SIMD3<Float>, direction: SIMD3<Float>) -> NodeHit? {
        var params = RaycastParams(origin: origin, direction: direction,
                                   nodeCount: UInt32(nodes.count))
        
        let resultBuffer = device.makeBuffer(length: MemoryLayout<RaycastResult>.stride,
                                              options: .storageModeShared)!
        
        let encoder = commandBuffer.makeComputeCommandEncoder()!
        encoder.setComputePipelineState(raycastPipeline)
        encoder.setBuffer(nodeBuffer, offset: 0, index: 0)
        encoder.setBytes(&params, length: MemoryLayout<RaycastParams>.stride, index: 1)
        encoder.setBuffer(resultBuffer, offset: 0, index: 2)
        
        let threads = MTLSize(width: nodes.count, height: 1, depth: 1)
        let threadgroup = MTLSize(width: min(nodes.count, 1024), height: 1, depth: 1)
        encoder.dispatchThreads(threads, threadsPerThreadgroup: threadgroup)
        encoder.endEncoding()
        commandBuffer.commit()
        commandBuffer.waitUntilCompleted()
        
        let result = resultBuffer.contents().load(as: RaycastResult.self)
        return result.hit ? NodeHit(nodeId: result.nodeId, distance: result.distance) : nil
    }
}
```

### Performance Requirements and Targets

```
Target: 90fps stereoscopic with 25k nodes
Frame budget: 11.1ms total
  - CPU encode: ≤2ms
  - GPU vertex: ≤4ms
  - GPU fragment: ≤4ms
  - Compositor overhead: ≤1ms

Memory limits:
  - macOS companion: ≤1GB total
  - GPU memory: ≤512MB (shared on Apple Silicon)
  - Per-frame CPU allocation: 0 (use pre-allocated ring buffers)

Draw call targets:
  - Nodes: 1 draw call (instanced)
  - Edges: 1 draw call (indexed)
  - UI overlay: ≤10 draw calls
  - Total: <20 per frame
```

### Metal Profiling Methodology

```
Tools:
1. Metal System Trace (Instruments):
   - GPU timeline with vertex/fragment breakdown
   - Memory bandwidth per pass
   - Shader occupancy

2. Shader Profiler:
   - Register count (>32 reduces occupancy)
   - Texture sample count
   - Memory access patterns

3. Frame Debugger:
   - Per-draw-call GPU time
   - Buffer contents inspection
   - Pipeline state validation

Key metrics to watch:
- Frame time in Metal System Trace (target: <11.1ms)
- GPU utilization (target: <80% for thermal headroom)
- Vertex shader occupancy (target: >75%)
- Memory bandwidth (bandwidth-limited = optimize access patterns)
```

## Scripts

### `scripts/metal_performance_checker.py`

Analyzes Metal performance data from Instruments exports and reports bottlenecks.

```
Usage: python metal_performance_checker.py instruments_export.json [--target-fps 90]
Input: JSON export from Instruments Metal System Trace
Output:
  - Frame time distribution (p50, p95, p99)
  - Frames below target (drop rate)
  - GPU stage breakdown (vertex/fragment/compute)
  - Memory bandwidth utilization
  - Recommended optimizations ranked by impact
```

### `scripts/shader_complexity_analyzer.py`

Estimates Metal shader complexity and predicts occupancy/performance characteristics.

```
Usage: python shader_complexity_analyzer.py shader.metal [--target-gpu apple-m2]
Input: .metal shader file
Output:
  - Estimated instruction count per stage
  - Sampler count (each sampler costs register space)
  - Branch complexity score
  - Predicted occupancy tier
  - Optimization suggestions with priority
```

## References

### `references/metal_best_practices.md`
Comprehensive Metal performance guide: buffer strategy (private vs shared vs managed), triple buffering implementation, draw call batching, compute shader optimization, memory heap management, and Apple Silicon-specific optimizations.

### `references/vision_pro_integration_guide.md`
Compositor Services API reference, RemoteImmersiveSpace setup, stereo frame pipeline, vergence-accommodation comfort zones, hand tracking APIs, and Human Interface Guidelines for spatial computing.

### `references/spatial_layout_algorithms.md`
Graph layout algorithm comparison: force-directed (Barnes-Hut optimization for GPU), hierarchical (Sugiyama framework), clustered (k-means preprocessing), and hybrid approaches — with GPU implementation notes for each.

## Assets

### `assets/metal_pipeline_template.swift`
Complete Metal rendering pipeline boilerplate: device setup, command queue, pipeline state compilation, triple-buffered uniform management, and render loop skeleton.

### `assets/compositor_services_template.swift`
Compositor Services integration template with stereo configuration, frame loop, depth texture setup, and RemoteImmersiveSpace connection boilerplate.

### `assets/metal_shader_templates.metal`
Shader library: instanced node vertex/fragment, edge geometry, GPU raycast compute, force-directed layout compute, with inline documentation.

## Quality Standards

- 90fps maintained in stereoscopic rendering with 25k nodes
- GPU utilization ≤80% for thermal headroom
- Memory usage ≤1GB on macOS companion
- <20 draw calls per frame
- Gaze-to-selection latency ≤50ms
- Zero frame drops during graph updates
- Spatial interactions feel immediate (≤1 frame latency)
