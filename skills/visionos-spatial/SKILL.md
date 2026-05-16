# visionOS Spatial Engineer Skill

## Overview

Provides native visionOS spatial computing patterns, SwiftUI volumetric interface design, Liquid Glass material implementation, and RealityKit integration for visionOS 26 applications. Covers WindowGroup management, spatial widget placement, gesture systems, observable entities, and accessibility in 3D space.

## Capabilities

### Liquid Glass Design System

**Glass Background Effect**
```swift
import SwiftUI

struct GlassPanel: View {
    var body: some View {
        VStack(spacing: 16) {
            Text("Spatial Interface")
                .font(.title)
            ControlGrid()
        }
        .padding(24)
        .glassBackgroundEffect()  // visionOS 26 Liquid Glass
    }
}

// Configurable display mode
struct AdaptiveGlassView: View {
    @Environment(\.colorScheme) var colorScheme
    
    var body: some View {
        ContentView()
            .glassBackgroundEffect(
                in: RoundedRectangle(cornerRadius: 20),
                displayMode: colorScheme == .dark ? .always : .implicit
            )
    }
}
```

**Spatial Typography**
```swift
// Depth-aware text that reads in 3D space
Text("Mission Control")
    .font(.system(size: 28, weight: .semibold, design: .rounded))
    .foregroundStyle(.primary)
    .shadow(color: .black.opacity(0.3), radius: 4, x: 0, y: 2)

// Dynamic type in volumetric context
struct SpatialLabel: View {
    let text: String
    var body: some View {
        Text(text)
            .font(.headline)
            .dynamicTypeSize(.large ... .accessibility2)  // Cap for legibility in 3D
    }
}
```

### WindowGroup Scene Architecture

**Unique Window Instance**
```swift
// visionOS 26: single-instance window (no duplicates)
@main
struct SpatialApp: App {
    var body: some Scene {
        // Main window — unique, persistent
        WindowGroup(id: "main") {
            ContentView()
        }
        .windowStyle(.plain)
        .defaultSize(width: 900, height: 600)
        
        // Volumetric window for 3D content
        WindowGroup(id: "spatial-view") {
            VolumetricContentView()
        }
        .windowStyle(.volumetric)
        .defaultSize(width: 0.6, height: 0.6, depth: 0.6, in: .meters)
        
        // Immersive space for full presence
        ImmersiveSpace(id: "immersive") {
            ImmersiveView()
        }
        .immersionStyle(selection: .constant(.mixed), in: .mixed)
    }
}

// Open windows programmatically
struct ContentView: View {
    @Environment(\.openWindow) var openWindow
    @Environment(\.openImmersiveSpace) var openImmersiveSpace
    
    var body: some View {
        Button("Open 3D View") {
            openWindow(id: "spatial-view")
        }
        Button("Enter Immersive") {
            Task { await openImmersiveSpace(id: "immersive") }
        }
    }
}
```

**Spatial Widget Placement**
```swift
// Widgets that snap to walls and tables persistently
struct SpatialWidgetConfiguration: Widget {
    var body: some WidgetConfiguration {
        StaticConfiguration(kind: "spatial.monitor", provider: MonitorProvider()) { entry in
            MonitorWidgetView(entry: entry)
                .containerBackground(.regularMaterial, for: .widget)
        }
        .configurationDisplayName("System Monitor")
        .description("Live metrics in your space")
        .supportedFamilies([.systemSmall, .systemMedium])
    }
}
```

### SwiftUI Volumetric APIs

**3D Content in Volumes**
```swift
struct VolumetricContentView: View {
    @State private var model = SpatialModel()
    
    var body: some View {
        RealityView { content in
            // Load 3D model into volume
            if let scene = try? await Entity(named: "SpatialScene") {
                content.add(scene)
            }
        } update: { content in
            // React to model changes
            if let entity = content.entities.first {
                entity.transform.rotation = model.rotation
            }
        }
        .gesture(rotateGesture)
        // Breakthrough: SwiftUI content pops outside volume boundary
        .overlay(alignment: .top) {
            BreakthroughLabel()
                .offset(z: 100)  // Extends beyond volume in Z
        }
    }
    
    var rotateGesture: some Gesture {
        RotateGesture3D()
            .onChanged { value in
                model.rotation = simd_quatf(value.rotation)
            }
    }
}
```

**Observable Entities (RealityKit + SwiftUI)**
```swift
// visionOS 26: entities as Observable objects
@Observable
class SpatialNode: Entity {
    var isSelected: Bool = false
    var label: String = ""
    
    required init() { super.init() }
}

struct EntityDrivenView: View {
    @State private var nodes: [SpatialNode] = []
    
    var body: some View {
        RealityView { content in
            for node in nodes {
                content.add(node)
            }
        }
        // SwiftUI automatically re-renders when observable entity changes
        .onChange(of: nodes.first?.isSelected) { _, selected in
            if selected == true { highlightSelected() }
        }
    }
}
```

**ViewAttachmentComponent**
```swift
// Attach SwiftUI views directly to RealityKit entities
struct AttachedLabelSystem: System {
    static let query = EntityQuery(where: .has(ViewAttachmentComponent.self))
    
    func update(context: SceneUpdateContext) {
        for entity in context.entities(matching: Self.query, updatingSystemWhen: .rendering) {
            // Labels follow their entities automatically
        }
    }
}

// Setup: attach SwiftUI view to entity
let labelEntity = ViewAttachmentEntity()
labelEntity.components[ViewAttachmentComponent.self] = ViewAttachmentComponent(
    attachmentID: "node-label"
)

RealityView { content, attachments in
    content.add(labelEntity)
} attachments: {
    Attachment(id: "node-label") {
        NodeLabelView(text: "Target Node")
            .glassBackgroundEffect()
    }
}
```

### Gesture Systems in Volumetric Space

**Gaze + Indirect Pinch**
```swift
struct SpatialInteractiveNode: View {
    @State private var isHovered = false
    
    var body: some View {
        RealityView { content in
            content.add(buildNodeEntity())
        }
        // Hover effect from gaze
        .hoverEffect { effect, isActive in
            effect.scaleEffect(isActive ? 1.1 : 1.0)
                  .opacity(isActive ? 1.0 : 0.8)
        }
        // Pinch to select
        .onTapGesture {
            handleSelection()
        }
        // Drag in 3D
        .gesture(
            DragGesture()
                .targetedToAnyEntity()
                .onChanged { value in
                    value.entity.position = value.convert(
                        value.location3D, from: .local, to: .scene
                    )
                }
        )
    }
}
```

**Direct Touch in Volumes**
```swift
// Hand mesh collision for direct manipulation
struct DirectTouchSurface: View {
    var body: some View {
        RealityView { content in
            let plane = ModelEntity(
                mesh: .generatePlane(width: 0.3, height: 0.2),
                materials: [PhysicallyBasedMaterial()]
            )
            // Enable direct touch input
            plane.components[InputTargetComponent.self] = InputTargetComponent(
                allowedInputTypes: [.direct, .indirect]
            )
            plane.components[CollisionComponent.self] = CollisionComponent(
                shapes: [.generateBox(width: 0.3, height: 0.2, depth: 0.01)]
            )
            content.add(plane)
        }
    }
}
```

### Multi-Window State Management

```swift
@Observable
class AppState {
    var openWindows: Set<String> = ["main"]
    var selectedEntity: Entity?
    var immersiveSpaceOpen = false
    
    func open(_ windowId: String) {
        openWindows.insert(windowId)
    }
    
    func close(_ windowId: String) {
        openWindows.remove(windowId)
    }
}

// Share state across windows via Environment
@main
struct SpatialApp: App {
    @State private var appState = AppState()
    
    var body: some Scene {
        WindowGroup(id: "main") {
            ContentView()
                .environment(appState)
        }
        WindowGroup(id: "detail") {
            DetailView()
                .environment(appState)  // Same instance, synchronized
        }
    }
}
```

### Performance for Spatial Content

```swift
// Efficient glass rendering — limit layered effects
struct PerformantGlassView: View {
    var body: some View {
        // ✅ One glassBackgroundEffect per container
        VStack {
            HeaderSection()
            ContentSection()
            FooterSection()
        }
        .glassBackgroundEffect()
        
        // ❌ Avoid: nested glass effects multiply GPU cost
        // VStack {
        //     HeaderSection().glassBackgroundEffect()
        //     ContentSection().glassBackgroundEffect()
        // }
    }
}

// Async entity loading — never block render thread
func loadScene() async {
    async let environment = Entity(named: "Environment")
    async let props = Entity(named: "Props")
    async let characters = Entity(named: "Characters")
    
    let (env, prop, char) = try await (environment, props, characters)
    // All loaded in parallel
    sceneRoot.addChild(env)
    sceneRoot.addChild(prop)
    sceneRoot.addChild(char)
}
```

## Scripts

### `scripts/visionos_window_layout_generator.py`

Generates visionOS WindowGroup scene configurations for spatial applications.

```
Usage: python visionos_window_layout_generator.py --windows [count] --style [plain|volumetric|immersive]
       python visionos_window_layout_generator.py --preset [dashboard|spatial|immersive-first]
       python visionos_window_layout_generator.py --format swift|json
Output:
  - Swift App scene declaration with WindowGroup configurations
  - Default size recommendations per window type
  - State management boilerplate for cross-window sync
  - Immersive space configuration with style options
```

### `scripts/liquid_glass_theme_checker.py`

Validates Liquid Glass implementation patterns and performance characteristics.

```
Usage: python liquid_glass_theme_checker.py [swift_file.swift]
       python liquid_glass_theme_checker.py --directory [src/]
Output:
  - Count of glassBackgroundEffect usage patterns
  - Nested glass effect warnings (performance risk)
  - Missing containerBackground for widget contexts
  - Accessibility contrast ratio estimates for glass overlays
  - Remediation suggestions ranked by performance impact
```

## References

### `references/visionos26_api_guide.md`
Complete visionOS 26 API reference: WindowGroup scene types, glassBackgroundEffect parameters, volumetric presentation APIs, spatial widget configuration, Observable entity patterns, ViewAttachmentComponent, and ImmersiveSpace styles.

### `references/liquid_glass_design_principles.md`
Apple's Liquid Glass design system: material properties, appropriate use contexts, contrast requirements for accessibility, dark/light adaptation, interaction states, and integration with system ornaments.

### `references/realitykit_swiftui_integration.md`
RealityKit-SwiftUI integration patterns: RealityView closures, attachment IDs, entity queries, collision shapes for input, hand tracking APIs, and async entity loading patterns.

## Assets

### `assets/spatial_app_template.swift`
Complete visionOS 26 app template: multi-window architecture, Liquid Glass panels, volumetric RealityView, immersive space, and shared Observable state.

### `assets/glass_component_library.swift`
Reusable Liquid Glass components: GlassCard, GlassSidebar, GlassToolbar, FloatingPanel, and SpatialModal with full accessibility support.

## Quality Standards

- Liquid Glass renders at 90fps without GPU over-budget
- No nested glassBackgroundEffect patterns (GPU cost)
- All interactive elements meet 44pt minimum touch target
- VoiceOver navigates spatial content with meaningful spatial descriptions
- Windows persist placement between sessions via scene storage
- Async entity loading prevents render thread blocking
- Observable state synchronizes across windows without race conditions
