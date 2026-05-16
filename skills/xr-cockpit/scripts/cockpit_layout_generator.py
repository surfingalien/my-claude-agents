#!/usr/bin/env python3
"""Generates A-Frame cockpit scene HTML with ergonomically positioned controls."""

import sys
import json
import argparse


# Ergonomic defaults: all in meters, relative to camera eye (0, 1.6, 0)
PRESETS = {
    "fighter": {
        "name": "Fighter Jet Cockpit",
        "dashboard_distance": 0.55,
        "dashboard_width": 1.0,
        "dashboard_height": 0.4,
        "controls": ["yoke", "throttle", "gauges", "toggles", "hud"],
    },
    "spacecraft": {
        "name": "Spacecraft Command Module",
        "dashboard_distance": 0.60,
        "dashboard_width": 1.4,
        "dashboard_height": 0.5,
        "controls": ["yoke", "throttle", "gauges", "toggles", "buttons", "screens"],
    },
    "submarine": {
        "name": "Submarine Bridge",
        "dashboard_distance": 0.65,
        "dashboard_width": 1.2,
        "dashboard_height": 0.45,
        "controls": ["throttle", "gauges", "toggles", "buttons"],
    },
    "command-center": {
        "name": "XR Command Center",
        "dashboard_distance": 0.70,
        "dashboard_width": 1.6,
        "dashboard_height": 0.55,
        "controls": ["gauges", "toggles", "buttons", "screens"],
    },
}

CONTROL_TEMPLATES = {
    "yoke": lambda: """      <!-- Yoke / Control Column -->
      <a-entity id="yoke"
        position="0 -0.18 -0.40"
        cockpit-joystick="pitchRange: -30 30; rollRange: -45 45; spring: 0.15">
        <a-cylinder radius="0.02" height="0.12" color="#2a2a2a"
          material="metalness: 0.8; roughness: 0.3"></a-cylinder>
        <a-entity position="0 0.06 0">
          <a-box width="0.18" height="0.02" depth="0.05" color="#333"
            material="metalness: 0.7"></a-box>
        </a-entity>
      </a-entity>""",

    "throttle": lambda: """      <!-- Throttle Lever -->
      <a-entity id="throttle-assembly" position="-0.45 -0.12 -0.45">
        <a-entity id="throttle-gate"
          geometry="primitive: box; width: 0.04; height: 0.25; depth: 0.06"
          material="color: #1a1a1a; metalness: 0.9"></a-entity>
        <a-entity id="throttle-lever" position="0 0 0.03"
          cockpit-lever="min: 0; max: 100; initial: 0; detents: 0 25 50 75 100">
          <a-box width="0.05" height="0.05" depth="0.08" color="#cc4400"
            material="roughness: 0.8"></a-box>
        </a-entity>
      </a-entity>""",

    "gauges": lambda: """      <!-- Gauge Cluster -->
      <a-entity id="gauges" position="0 0.04 -0.52">
        <a-entity position="-0.15 0 0" cockpit-gauge="label: ALT; min: 0; max: 50000; value: 0; color: #00ff88"></a-entity>
        <a-entity position="0 0 0"     cockpit-gauge="label: SPD; min: 0; max: 600; value: 0; warningThreshold: 80; dangerThreshold: 95"></a-entity>
        <a-entity position="0.15 0 0"  cockpit-gauge="label: FUEL; min: 0; max: 100; value: 75; warningThreshold: 25; dangerThreshold: 10; color: #ffaa00"></a-entity>
      </a-entity>""",

    "toggles": lambda: """      <!-- Toggle Switch Array -->
      <a-entity id="toggles" position="0.40 0.02 -0.46">
        <a-entity position="0    0    0" cockpit-toggle="label: PWR; state: true"></a-entity>
        <a-entity position="0.05 0    0" cockpit-toggle="label: NAV"></a-entity>
        <a-entity position="0.10 0    0" cockpit-toggle="label: COM"></a-entity>
        <a-entity position="0    -0.06 0" cockpit-toggle="label: AUX"></a-entity>
        <a-entity position="0.05 -0.06 0" cockpit-toggle="label: ECO"></a-entity>
      </a-entity>""",

    "buttons": lambda: """      <!-- Push Button Array -->
      <a-entity id="buttons" position="-0.30 0.02 -0.48">
        <a-entity position="0    0 0"    cockpit-button="label: FIRE; color: #ff2244"></a-entity>
        <a-entity position="0.07 0 0"    cockpit-button="label: ARM"></a-entity>
        <a-entity position="0.14 0 0"    cockpit-button="label: SAFE; color: #00aa44"></a-entity>
      </a-entity>""",

    "hud": lambda: """      <!-- HUD Overlay (transparent plane) -->
      <a-entity id="hud" position="0 0.12 -0.48">
        <a-plane width="0.60" height="0.20"
          material="color: #00ff88; opacity: 0.15; transparent: true; side: double">
        </a-plane>
        <a-text value="HDG: 090  ALT: 5000  SPD: 250"
          align="center" color="#00ff88" width="0.8"
          position="0 0 0.002"></a-text>
      </a-entity>""",

    "screens": lambda: """      <!-- MFD Screens -->
      <a-entity id="screens" position="0 0 -0.54">
        <a-plane id="mfd-left"  position="-0.25 0 0" width="0.22" height="0.18"
          material="color: #001122; emissive: #002244; roughness: 1"></a-plane>
        <a-plane id="mfd-right" position="0.25 0 0"  width="0.22" height="0.18"
          material="color: #001122; emissive: #002244; roughness: 1"></a-plane>
      </a-entity>""",
}


def validate_placement(controls: list[str], distance: float) -> list[dict]:
    issues = []
    if distance < 0.35:
        issues.append({"control": "dashboard", "issue": "Too close (<35cm) — eye strain risk"})
    if distance > 0.80:
        issues.append({"control": "dashboard", "issue": "Too far (>80cm) — hard to reach"})
    if "yoke" in controls and distance > 0.65:
        issues.append({"control": "yoke", "issue": "Yoke too far — move within 55-65cm"})
    return issues


def generate_html(preset_name: str, config: dict, seat_count: int) -> str:
    controls = config["controls"]
    dist = config["dashboard_distance"]
    w = config["dashboard_width"]
    h = config["dashboard_height"]

    control_html = "\n".join(
        CONTROL_TEMPLATES[c]()
        for c in controls
        if c in CONTROL_TEMPLATES
    )

    issues = validate_placement(controls, dist)
    issue_comments = "\n".join(
        f"      <!-- ERGONOMICS WARNING: {i['control']} — {i['issue']} -->"
        for i in issues
    ) if issues else "      <!-- Ergonomics: all controls within comfortable reach zone -->"

    return f"""<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <title>{config['name']}</title>
  <script src="https://aframe.io/releases/1.5.0/aframe.min.js"></script>
  <script src="cockpit_components.js"></script>
</head>
<body>

<a-scene background="color: #0a0a0f" renderer="antialias: true">

  <!-- Audio Assets -->
  <a-assets>
    <audio id="click-on"  src="audio/switch_on.wav"  preload="auto"></audio>
    <audio id="click-off" src="audio/switch_off.wav" preload="auto"></audio>
    <audio id="button-press" src="audio/button.wav"  preload="auto"></audio>
  </a-assets>

  <!-- Player Rig -->
  <a-entity id="rig" position="0 0 0">
    <a-camera id="camera" position="0 1.6 0" look-controls="pointerLockEnabled: false">

      <!-- Cockpit Frame (camera-attached) -->
      <a-entity id="cockpit-frame" position="0 -0.30 -{dist:.2f}">

        {issue_comments}

        <!-- Main Dashboard Panel -->
        <a-plane id="dashboard"
          width="{w:.2f}" height="{h:.2f}"
          position="0 0 0"
          material="color: #111118; metalness: 0.85; roughness: 0.15; side: front"
          shadow="cast: false">
        </a-plane>

        <!-- Dashboard Edge Trim -->
        <a-box width="{w+0.02:.2f}" height="0.01" depth="0.02"
          position="0 {h/2:.2f} 0.01"
          material="color: #444; metalness: 0.9"></a-box>

{control_html}

      </a-entity>
    </a-camera>
  </a-entity>

  <!-- Environment -->
  <a-sky color="#050510"></a-sky>
  <a-entity light="type: ambient; intensity: 0.3; color: #223355"></a-entity>
  <a-entity light="type: directional; intensity: 0.8" position="1 3 2"></a-entity>
  <!-- Cockpit accent lighting -->
  <a-entity light="type: point; intensity: 0.5; color: #00ff88; distance: 1"
    position="0 1.4 -0.6"></a-entity>

</a-scene>
</body>
</html>"""


def main():
    parser = argparse.ArgumentParser(
        description="Generate A-Frame cockpit scene with ergonomic control layout",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            "Usage:\n"
            "  python cockpit_layout_generator.py --preset fighter\n"
            "  python cockpit_layout_generator.py --preset spacecraft --format json\n"
            "  python cockpit_layout_generator.py --controls yoke,throttle,gauges --seats 1"
        )
    )
    parser.add_argument("--preset", choices=list(PRESETS.keys()),
                        help="Predefined cockpit preset")
    parser.add_argument("--controls", help="Comma-separated control list: yoke,throttle,gauges,toggles,buttons,hud,screens")
    parser.add_argument("--seats", type=int, default=1)
    parser.add_argument("--format", choices=["html", "json"], default="html")
    args = parser.parse_args()

    if args.preset:
        config = PRESETS[args.preset]
        preset_name = args.preset
    else:
        controls = [c.strip() for c in (args.controls or "gauges,toggles").split(",")]
        config = {
            "name": "Custom Cockpit",
            "dashboard_distance": 0.55,
            "dashboard_width": 1.0,
            "dashboard_height": 0.4,
            "controls": controls,
        }
        preset_name = "custom"

    if args.format == "json":
        issues = validate_placement(config["controls"], config["dashboard_distance"])
        output = {
            "preset": preset_name,
            "config": config,
            "ergonomics": {
                "dashboard_distance_m": config["dashboard_distance"],
                "validation_issues": issues,
                "comfort_score": max(0, 100 - len(issues) * 20),
                "reach_zone": "primary" if 0.40 <= config["dashboard_distance"] <= 0.65 else "secondary",
            },
            "controls": config["controls"],
        }
        print(json.dumps(output, indent=2))
    else:
        print(generate_html(preset_name, config, args.seats))


if __name__ == "__main__":
    main()
