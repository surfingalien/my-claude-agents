# XR Cockpit Interaction Specialist Skill

## Overview

Provides cockpit-based immersive control system design for XR environments using A-Frame and Three.js. Covers fixed-perspective interaction zones, constraint-driven control mechanics, seated ergonomics for motion comfort, dashboard UI with animated feedback, and multi-input integration (hand gestures, gaze, voice, physical props).

## Capabilities

### Cockpit Architecture Patterns

**Fixed-Perspective Scene Setup (A-Frame)**
```html

<a-scene>
  
  <a-entity id="rig" position="0 0 0">
    <a-camera id="camera" position="0 1.6 0" look-controls>
      
      
      <a-entity id="cockpit-frame" position="0 -0.3 -0.6">
        
        
        <a-entity id="dashboard" 
          geometry="primitive: plane; width: 1.2; height: 0.5"
          position="0 0 0"
          material="color: #1a1a2e; metalness: 0.8; roughness: 0.2">
        </a-entity>
        
        
        <a-entity id="left-console" position="-0.55 -0.1 0.05" 
          rotation="0 25 -10">
        </a-entity>
        
        
        <a-entity id="right-console" position="0.55 -0.1 0.05"
          rotation="0 -25 10">
        </a-entity>
        
      </a-entity>
    </a-camera>
  </a-entity>
</a-scene>
```

**Ergonomic Reach Zones**
```javascript
// Comfort zones for seated XR (measured from seated eye position)
const REACH_ZONES = {
  // Primary zone: effortless reach, zero discomfort
  primary: {
    distance: { min: 0.4, max: 0.65 },  // meters from eye
    elevation: { min: -20, max: 15 },     // degrees from horizontal
    horizontal: { min: -35, max: 35 }     // degrees from center
  },
  // Secondary zone: reachable with slight effort
  secondary: {
    distance: { min: 0.3, max: 0.8 },
    elevation: { min: -30, max: 25 },
    horizontal: { min: -55, max: 55 }
  },
  // Danger zone: avoid for frequent controls (motion sickness risk)
  avoid: {
    elevation: { above: 30, below: -40 }
  }
};

function validateControlPlacement(control) {
  const { distance, elevation, horizontal } = control.position;
  if (elevation > REACH_ZONES.avoid.elevation.above) {
    console.warn(`${control.id}: too high — motion sickness risk`);
    return false;
  }
  return distance >= REACH_ZONES.primary.distance.min && 
         distance <= REACH_ZONES.primary.distance.max;
}
```

### Constraint-Driven Control Mechanics

**Yoke/Joystick with Axis Constraints**
```javascript
// Constrained input — no free-float, physics-accurate feel
class ConstrainedYoke extends THREE.Object3D {
  constructor(options = {}) {
    super();
    this.pitchRange = options.pitchRange || [-30, 30];  // degrees
    this.rollRange = options.rollRange || [-45, 45];
    this.currentPitch = 0;
    this.currentRoll = 0;
    this.springStrength = options.spring || 0.15;  // Return-to-center force
    this.deadzone = options.deadzone || 2;  // degrees
  }

  applyInput(deltaPitch, deltaRoll) {
    // Clamp to physical limits
    this.currentPitch = THREE.MathUtils.clamp(
      this.currentPitch + deltaPitch,
      this.pitchRange[0], this.pitchRange[1]
    );
    this.currentRoll = THREE.MathUtils.clamp(
      this.currentRoll + deltaRoll,
      this.rollRange[0], this.rollRange[1]
    );
    
    // Update visual rotation
    this.rotation.x = THREE.MathUtils.degToRad(this.currentPitch);
    this.rotation.z = THREE.MathUtils.degToRad(this.currentRoll);
    
    return {
      pitch: this.currentPitch / this.pitchRange[1],  // Normalized -1 to 1
      roll: this.currentRoll / this.rollRange[1]
    };
  }

  update(deltaTime) {
    // Spring return to center when released
    if (Math.abs(this.currentPitch) > this.deadzone) {
      this.currentPitch *= (1 - this.springStrength);
    } else {
      this.currentPitch = 0;
    }
    if (Math.abs(this.currentRoll) > this.deadzone) {
      this.currentRoll *= (1 - this.springStrength);
    } else {
      this.currentRoll = 0;
    }
    this.rotation.x = THREE.MathUtils.degToRad(this.currentPitch);
    this.rotation.z = THREE.MathUtils.degToRad(this.currentRoll);
  }
}
```

**Throttle Lever (Linear Constraint)**
```javascript
class ThrottleLever {
  constructor(el, options = {}) {
    this.el = el;
    this.min = options.min || 0;
    this.max = options.max || 100;
    this.value = options.initial || 0;
    this.detents = options.detents || [0, 25, 50, 75, 100];  // Tactile stops
    this.detentStrength = options.detentStrength || 8;  // Degrees snap range
    
    // Visual travel range in world space
    this.minY = -0.12;  // meters down from neutral
    this.maxY = 0.12;   // meters up from neutral
  }

  setValue(rawValue) {
    let snapped = this.snapToDetent(rawValue);
    this.value = THREE.MathUtils.clamp(snapped, this.min, this.max);
    
    // Update visual position
    const t = (this.value - this.min) / (this.max - this.min);
    this.el.object3D.position.y = THREE.MathUtils.lerp(this.minY, this.maxY, t);
    
    return this.value;
  }

  snapToDetent(value) {
    for (const detent of this.detents) {
      if (Math.abs(value - detent) < this.detentStrength) return detent;
    }
    return value;
  }
}
```

### Dashboard UI with Animated Feedback

**Gauge Component (A-Frame)**
```javascript
AFRAME.registerComponent('cockpit-gauge', {
  schema: {
    value: { type: 'number', default: 0 },
    min: { type: 'number', default: 0 },
    max: { type: 'number', default: 100 },
    label: { type: 'string', default: 'GAUGE' },
    warningThreshold: { type: 'number', default: 80 },
    dangerThreshold: { type: 'number', default: 95 },
    color: { type: 'color', default: '#00ff88' }
  },

  init() {
    this.needle = this.el.querySelector('.needle');
    this.valueDisplay = this.el.querySelector('.value-text');
    this.prevValue = 0;
  },

  update() {
    const { value, min, max, warningThreshold, dangerThreshold } = this.data;
    const normalized = (value - min) / (max - min);
    
    // Needle rotation: -135° (min) to +135° (max)
    const degrees = -135 + (normalized * 270);
    
    // Smooth animation via lerp
    const smoothed = THREE.MathUtils.lerp(this.prevValue, degrees, 0.1);
    this.needle.setAttribute('rotation', `0 0 ${smoothed}`);
    this.prevValue = smoothed;
    
    // Color state: normal → warning → danger
    const pct = value / max * 100;
    const color = pct >= dangerThreshold ? '#ff2244' :
                  pct >= warningThreshold ? '#ffaa00' : this.data.color;
    this.needle.setAttribute('material', `color: ${color}`);
    this.valueDisplay.setAttribute('value', Math.round(value).toString());
  }
});
```

**Toggle Switch with Audio Feedback**
```javascript
AFRAME.registerComponent('cockpit-toggle', {
  schema: {
    state: { type: 'boolean', default: false },
    label: { type: 'string', default: 'SYS' },
    soundOn: { type: 'string', default: '#click-on' },
    soundOff: { type: 'string', default: '#click-off' }
  },

  init() {
    this.el.addEventListener('click', this.toggle.bind(this));
    this.updateVisuals(this.data.state);
  },

  toggle() {
    this.data.state = !this.data.state;
    this.updateVisuals(this.data.state);
    
    // Tactile audio feedback
    const sound = this.data.state ? this.data.soundOn : this.data.soundOff;
    this.el.sceneEl.querySelector(sound)?.components.sound.playSound();
    
    this.el.emit('toggle-changed', { state: this.data.state });
  },

  updateVisuals(state) {
    const knob = this.el.querySelector('.knob');
    knob?.setAttribute('position', `0 ${state ? 0.015 : -0.015} 0`);
    this.el.querySelector('.indicator')?.setAttribute(
      'material', `color: ${state ? '#00ff88' : '#333'}`
    );
  }
});
```

### Multi-Input Integration

**Gaze + Dwell Selection**
```javascript
AFRAME.registerComponent('gaze-interact', {
  schema: {
    dwellTime: { type: 'number', default: 1500 },  // ms before auto-select
    showProgress: { type: 'boolean', default: true }
  },

  init() {
    this.gazeStart = null;
    this.progressRing = this.el.querySelector('.gaze-ring');
    
    this.el.addEventListener('mouseenter', () => {
      this.gazeStart = Date.now();
      if (this.progressRing) this.progressRing.setAttribute('visible', true);
    });
    
    this.el.addEventListener('mouseleave', () => {
      this.gazeStart = null;
      this.resetProgress();
    });
  },

  tick() {
    if (!this.gazeStart) return;
    const elapsed = Date.now() - this.gazeStart;
    const progress = Math.min(elapsed / this.data.dwellTime, 1);
    
    if (this.progressRing) {
      this.progressRing.setAttribute('theta-length', progress * 360);
    }
    
    if (progress >= 1) {
      this.el.emit('gaze-selected');
      this.gazeStart = null;
      this.resetProgress();
    }
  },

  resetProgress() {
    if (this.progressRing) {
      this.progressRing.setAttribute('theta-length', 0);
      this.progressRing.setAttribute('visible', false);
    }
  }
});
```

**Voice Command Integration**
```javascript
class CockpitVoiceControl {
  constructor(cockpit) {
    this.cockpit = cockpit;
    this.commands = new Map([
      ['autopilot engage', () => cockpit.setAutopilot(true)],
      ['autopilot disengage', () => cockpit.setAutopilot(false)],
      ['gear down', () => cockpit.setGear('down')],
      ['gear up', () => cockpit.setGear('up')],
      ['flaps full', () => cockpit.setFlaps(100)],
      ['flaps up', () => cockpit.setFlaps(0)],
    ]);
    
    this.recognition = new window.SpeechRecognition();
    this.recognition.continuous = true;
    this.recognition.interimResults = false;
    
    this.recognition.onresult = (event) => {
      const transcript = event.results[event.results.length - 1][0].transcript
        .toLowerCase().trim();
      
      for (const [command, action] of this.commands) {
        if (transcript.includes(command)) {
          action();
          cockpit.announceCommand(command);
          break;
        }
      }
    };
  }

  start() { this.recognition.start(); }
  stop() { this.recognition.stop(); }
}
```

## Scripts

### `scripts/cockpit_layout_generator.py`

Generates A-Frame cockpit scene HTML with ergonomically positioned controls.

```
Usage: python cockpit_layout_generator.py --preset [fighter|spacecraft|submarine|command-center]
       python cockpit_layout_generator.py --controls yoke,throttle,gauges,toggles --seats 1
       python cockpit_layout_generator.py --format html|json
Output:
  - Complete A-Frame scene HTML with cockpit geometry
  - Control placement within ergonomic reach zones
  - Dashboard gauge and toggle components
  - Audio feedback asset declarations
  - Comfort validation report (distance, elevation, horizontal angle)
```

### `scripts/motion_comfort_analyzer.py`

Analyzes cockpit control placement against motion sickness thresholds.

```
Usage: python motion_comfort_analyzer.py cockpit_layout.json
       python motion_comfort_analyzer.py --interactive (guided placement wizard)
Output:
  - Per-control comfort score (0-100)
  - Zone classification (primary/secondary/avoid)
  - Head movement range required (< 30° recommended)
  - Controls outside safe elevation band (flagged)
  - Redesign suggestions for flagged controls
```

## References

### `references/xr_ergonomics_guide.md`
Seated XR interaction design: comfortable viewing distances (0.5–2m for text), FOV considerations (100° horizontal for most headsets), head rotation limits (±35° for comfort), reach zones for hand interaction, and vestibular conflict minimization patterns.

### `references/cockpit_design_standards.md`
Real cockpit design principles adapted for XR: instrument panel hierarchy (primary flight instruments center), control accessibility (critical controls within primary reach zone), feedback modalities (visual + audio + haptic), and emergency control placement conventions.

### `references/aframe_component_patterns.md`
A-Frame component architecture for cockpit systems: schema design, event bubbling patterns, multi-component coordination, performance optimization (avoid tick() abuse), and WebXR controller input mapping.

## Assets

### `assets/cockpit_scene_template.html`
Complete A-Frame cockpit scene: camera rig, dashboard panel, left/right consoles, yoke, throttle, gauge cluster, toggle array, and ambient lighting with audio assets.

### `assets/cockpit_components.js`
Production A-Frame components: cockpit-gauge, cockpit-toggle, cockpit-lever, gaze-interact, voice-control, constraint-joystick with full event emission.

## Quality Standards

- Zero motion sickness for seated sessions of 30+ minutes
- All primary controls within primary reach zone (±35° horizontal, -20°/+15° elevation)
- Control response latency ≤50ms (input to visual feedback)
- Audio feedback on every toggle/lever state change
- Graceful degradation: gaze fallback when hand tracking unavailable
- Voice commands active only when headset microphone available
- Frame rate maintained at target device Hz (72/90/120fps) during control animation
