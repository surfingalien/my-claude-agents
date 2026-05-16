# WebXR Immersive Developer Skill

## Overview

Provides browser-based AR/VR/XR development expertise using WebXR Device API, A-Frame, Three.js, and Babylon.js. Covers immersive session management, hand tracking, raycasting hit testing, real-time physics, LOD systems, cross-device compatibility (Meta Quest, Vision Pro, HoloLens, mobile AR), and graceful degradation strategies.

## Capabilities

### WebXR Session Management

**Immersive Session Setup**
```javascript
// Feature detect and request XR session
async function initXR() {
  if (!navigator.xr) {
    showFallback('WebXR not supported — use a compatible browser');
    return;
  }
  
  const supported = await navigator.xr.isSessionSupported('immersive-vr');
  if (!supported) {
    const arSupported = await navigator.xr.isSessionSupported('immersive-ar');
    if (!arSupported) {
      showFallback('Immersive XR not available on this device');
      return;
    }
  }
  
  const mode = supported ? 'immersive-vr' : 'immersive-ar';
  
  const session = await navigator.xr.requestSession(mode, {
    requiredFeatures: ['local-floor'],
    optionalFeatures: [
      'hand-tracking',
      'bounded-floor',
      'dom-overlay',     // AR: render HTML over camera
      'depth-sensing',   // AR: real-world depth
      'hit-test',        // AR: surface placement
      'layers',          // Efficient quad layers
    ]
  });
  
  return session;
}
```

**Render Loop**
```javascript
class XRRenderer {
  constructor(session, scene, camera) {
    this.session = session;
    this.scene = scene;
    this.camera = camera;
    
    // WebXR-compatible renderer
    this.renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
    this.renderer.xr.enabled = true;
    this.renderer.xr.setSession(session);
    this.renderer.xr.setReferenceSpaceType('local-floor');
    
    this.clock = new THREE.Clock();
  }
  
  start() {
    this.renderer.setAnimationLoop((timestamp, frame) => {
      if (!frame) return;
      
      const delta = this.clock.getDelta();
      this.update(delta, frame);
      this.renderer.render(this.scene, this.camera);
    });
  }
  
  update(delta, frame) {
    // Override with per-frame logic
  }
  
  end() {
    this.renderer.setAnimationLoop(null);
    this.session.end();
  }
}
```

### Hand Tracking

**Full Hand Skeleton**
```javascript
const HAND_JOINTS = [
  'wrist',
  'thumb-metacarpal', 'thumb-phalanx-proximal', 'thumb-phalanx-distal', 'thumb-tip',
  'index-finger-metacarpal', 'index-finger-phalanx-proximal',
  'index-finger-phalanx-intermediate', 'index-finger-phalanx-distal', 'index-finger-tip',
  // ... other fingers follow same pattern
];

class HandTracker {
  constructor(session, referenceSpace) {
    this.session = session;
    this.referenceSpace = referenceSpace;
    this.hands = { left: null, right: null };
    this.jointMeshes = { left: {}, right: {} };
  }

  update(frame) {
    for (const inputSource of this.session.inputSources) {
      if (!inputSource.hand) continue;
      const hand = inputSource.hand;
      const handedness = inputSource.handedness;
      
      for (const [jointName, joint] of hand) {
        const jointPose = frame.getJointPose(joint, this.referenceSpace);
        if (!jointPose) continue;
        
        // Update joint mesh transform
        const mesh = this.jointMeshes[handedness][jointName];
        if (mesh) {
          mesh.position.copy(jointPose.transform.position);
          mesh.quaternion.copy(jointPose.transform.orientation);
          mesh.scale.setScalar(jointPose.radius || 0.01);
        }
      }
    }
  }

  getPinchStrength(handedness, frame) {
    const source = [...this.session.inputSources]
      .find(s => s.handedness === handedness && s.hand);
    if (!source) return 0;
    
    const thumbTip = frame.getJointPose(
      source.hand.get('thumb-tip'), this.referenceSpace
    );
    const indexTip = frame.getJointPose(
      source.hand.get('index-finger-tip'), this.referenceSpace
    );
    
    if (!thumbTip || !indexTip) return 0;
    
    const distance = new THREE.Vector3()
      .copy(thumbTip.transform.position)
      .distanceTo(indexTip.transform.position);
    
    // Normalize: 0 = fully pinched (< 2cm), 1 = open
    return Math.max(0, 1 - (distance / 0.04));
  }
}
```

### Raycasting and Hit Testing

**Controller Raycast**
```javascript
class XRRaycaster {
  constructor(scene) {
    this.scene = scene;
    this.raycaster = new THREE.Raycaster();
    this.tempMatrix = new THREE.Matrix4();
  }

  castFromController(controller) {
    // Get ray direction from controller
    this.tempMatrix.identity().extractRotation(controller.matrixWorld);
    
    this.raycaster.ray.origin.setFromMatrixPosition(controller.matrixWorld);
    this.raycaster.ray.direction.set(0, 0, -1).applyMatrix4(this.tempMatrix);
    
    return this.raycaster.intersectObjects(this.scene.children, true);
  }

  castFromGaze(camera) {
    // Center screen raycast for gaze-based targeting
    this.raycaster.setFromCamera(new THREE.Vector2(0, 0), camera);
    return this.raycaster.intersectObjects(this.scene.children, true);
  }
}
```

**AR Hit Testing (Surface Placement)**
```javascript
class ARHitTester {
  constructor(session, renderer) {
    this.session = session;
    this.renderer = renderer;
    this.hitTestSource = null;
    this.reticle = this.createReticle();
  }

  async init() {
    const viewerSpace = await this.session.requestReferenceSpace('viewer');
    this.hitTestSource = await this.session.requestHitTestSource({
      space: viewerSpace
    });
  }

  update(frame, referenceSpace) {
    if (!this.hitTestSource) return;
    
    const results = frame.getHitTestResults(this.hitTestSource);
    if (results.length > 0) {
      const pose = results[0].getPose(referenceSpace);
      this.reticle.visible = true;
      this.reticle.matrix.fromArray(pose.transform.matrix);
    } else {
      this.reticle.visible = false;
    }
  }

  placeObject(object) {
    if (!this.reticle.visible) return false;
    object.position.copy(this.reticle.position);
    object.quaternion.copy(this.reticle.quaternion);
    return true;
  }

  createReticle() {
    const geometry = new THREE.RingGeometry(0.08, 0.1, 32);
    const material = new THREE.MeshBasicMaterial({ side: THREE.DoubleSide });
    const mesh = new THREE.Mesh(geometry, material);
    mesh.matrixAutoUpdate = false;
    mesh.visible = false;
    return mesh;
  }
}
```

### Performance Optimization

**LOD System**
```javascript
class XRLODSystem {
  constructor(camera, thresholds = { high: 2, medium: 8, low: 20 }) {
    this.camera = camera;
    this.thresholds = thresholds;
    this.lodObjects = [];
  }

  add(position, { highDetail, mediumDetail, lowDetail }) {
    this.lodObjects.push({
      position: position.clone(),
      levels: { high: highDetail, medium: mediumDetail, low: lowDetail },
      current: 'high'
    });
    return highDetail;  // Return highest LOD for initial rendering
  }

  update() {
    const camPos = this.camera.position;
    
    for (const obj of this.lodObjects) {
      const distance = camPos.distanceTo(obj.position);
      
      const newLevel = distance < this.thresholds.high ? 'high' :
                       distance < this.thresholds.medium ? 'medium' : 'low';
      
      if (newLevel !== obj.current) {
        obj.levels[obj.current].visible = false;
        obj.levels[newLevel].visible = true;
        obj.current = newLevel;
      }
    }
  }
}
```

**Occlusion Culling**
```javascript
class FrustumCuller {
  constructor(camera) {
    this.camera = camera;
    this.frustum = new THREE.Frustum();
    this.projScreenMatrix = new THREE.Matrix4();
  }

  cull(objects) {
    this.projScreenMatrix.multiplyMatrices(
      this.camera.projectionMatrix,
      this.camera.matrixWorldInverse
    );
    this.frustum.setFromProjectionMatrix(this.projScreenMatrix);
    
    for (const obj of objects) {
      if (obj.geometry?.boundingSphere) {
        obj.visible = this.frustum.intersectsSphere(
          obj.geometry.boundingSphere.clone().applyMatrix4(obj.matrixWorld)
        );
      }
    }
  }
}
```

### Cross-Device Compatibility

**Device Capability Detection**
```javascript
class XRDeviceProfile {
  static async detect() {
    const profile = {
      supportsVR: await navigator.xr?.isSessionSupported('immersive-vr'),
      supportsAR: await navigator.xr?.isSessionSupported('immersive-ar'),
      supportsHandTracking: false,
      supportsControllers: false,
      performanceTier: 'unknown'
    };
    
    // Infer device from UA + GPU
    const renderer = new THREE.WebGLRenderer();
    const info = renderer.getContext().getParameter(
      renderer.getContext().RENDERER
    );
    renderer.dispose();
    
    profile.gpu = info;
    
    if (info.includes('Quest')) {
      profile.performanceTier = 'mid';
      profile.supportsHandTracking = true;
    } else if (info.includes('Apple')) {
      profile.performanceTier = 'high';
    } else if (info.includes('Adreno 6') || info.includes('Mali-G7')) {
      profile.performanceTier = 'low';
    }
    
    return profile;
  }

  static recommendQuality(profile) {
    const settings = {
      high: { shadows: true, antialias: true, maxPolygons: 500000, textureSize: 2048 },
      mid:  { shadows: false, antialias: true, maxPolygons: 200000, textureSize: 1024 },
      low:  { shadows: false, antialias: false, maxPolygons: 50000, textureSize: 512 }
    };
    return settings[profile.performanceTier] || settings.low;
  }
}
```

**Graceful Degradation**
```javascript
class XRExperienceFallback {
  static async init(containerEl) {
    // Try immersive XR first
    if (await navigator.xr?.isSessionSupported('immersive-vr')) {
      return new ImmersiveVRExperience(containerEl);
    }
    
    // Try AR
    if (await navigator.xr?.isSessionSupported('immersive-ar')) {
      return new ImmersiveARExperience(containerEl);
    }
    
    // Inline session (mobile gyro, no headset)
    if (await navigator.xr?.isSessionSupported('inline')) {
      return new InlineXRExperience(containerEl);
    }
    
    // Full 3D fallback — mouse/touch orbit, no XR
    return new Desktop3DExperience(containerEl);
  }
}
```

### A-Frame Integration Patterns

```javascript
// Register custom WebXR-aware A-Frame component
AFRAME.registerComponent('webxr-interactive', {
  schema: {
    interactionMode: { type: 'string', default: 'auto' }  // auto|hand|controller|gaze
  },

  init() {
    this.session = null;
    this.el.sceneEl.addEventListener('enter-vr', () => {
      this.session = this.el.sceneEl.xrSession;
      this.detectInputMode();
    });
  },

  detectInputMode() {
    if (!this.session) return;
    
    const hasHands = [...this.session.inputSources].some(s => s.hand);
    const hasControllers = [...this.session.inputSources].some(
      s => s.targetRayMode === 'tracked-pointer'
    );
    
    this.activeMode = hasHands ? 'hand' : hasControllers ? 'controller' : 'gaze';
    this.el.emit('input-mode-detected', { mode: this.activeMode });
  }
});
```

## Scripts

### `scripts/webxr_compatibility_checker.py`

Checks WebXR feature support matrix across target browsers and devices.

```
Usage: python webxr_compatibility_checker.py --target [quest2|quest3|vision-pro|hololens2|mobile-ar]
       python webxr_compatibility_checker.py --features hand-tracking,hit-test,depth-sensing
       python webxr_compatibility_checker.py --browser [chrome|safari|firefox]
Output:
  - Feature support matrix per device/browser combination
  - Required polyfills for missing features
  - Fallback strategy recommendations per feature gap
  - Minimum browser version requirements
  - Performance tier estimates per target device
```

### `scripts/xr_performance_profiler.py`

Analyzes WebXR frame timing data and identifies performance bottlenecks.

```
Usage: python xr_performance_profiler.py timing_data.json [--target-fps 72]
       python xr_performance_profiler.py --from-console (paste console log data)
Output:
  - Frame time distribution (p50, p95, p99)
  - Drop rate below target FPS
  - CPU vs GPU time split estimate
  - Draw call count analysis
  - Memory usage trend
  - Top optimization suggestions with estimated impact
```

## References

### `references/webxr_device_api_guide.md`
Complete WebXR Device API reference: session modes (inline, immersive-vr, immersive-ar), reference space types (viewer, local, local-floor, bounded-floor), frame loop, input sources, hit testing, and DOM overlay for AR.

### `references/cross_device_compat_matrix.md`
Browser × device compatibility: Chrome/Edge on Quest (WebXR full support), Safari on Vision Pro (WebXR experimental), HoloLens (Edge, limited), Chrome Android (immersive-ar via ARCore), iOS Safari (inline + limited AR). Feature support and workarounds for each combination.

### `references/webxr_performance_guide.md`
WebXR performance optimization: single-pass stereo rendering, instanced mesh for repeated objects, texture atlas strategy, avoiding main-thread blocking during XR loop, requestAnimationFrame vs XR frame loop interaction, and GPU memory budget per device tier.

## Assets

### `assets/webxr_project_template/`
Complete WebXR starter project: index.html, renderer setup, session management, hand tracking module, controller input, AR hit testing, LOD system, and device fallback logic.

### `assets/aframe_xr_scene_template.html`
A-Frame scene with full WebXR integration: VR/AR mode support, hand tracking avatars, controller ray visualization, gaze cursor fallback, and performance monitoring HUD.

## Quality Standards

- Immersive session loads in ≤3 seconds on target devices
- Frame rate at or above device refresh rate (72/90/120Hz) at p95
- Graceful degradation: every feature has a non-XR fallback
- Hand tracking responds within 1 frame of pose update
- AR hit test reticle updates every frame without stutter
- Cross-browser tested: Chrome (Quest), Safari (Vision Pro), Edge (HoloLens)
- No WebXR session leaks: session.end() called on all exit paths
