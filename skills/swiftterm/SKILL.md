# SwiftTerm Skill

## Overview

Provides SwiftTerm integration patterns, terminal emulation expertise, text rendering optimization, and SSH I/O bridging for Swift applications on iOS, macOS, and visionOS. Covers VT100/xterm ANSI escape sequences, UTF-8 rendering, scrollback management, theming, accessibility, and multi-session management.

## Capabilities

### SwiftTerm Integration Patterns

**SwiftUI Embedding**
```swift
import SwiftTerm
import SwiftUI

// Embed SwiftTerm in a SwiftUI view
struct TerminalView: UIViewRepresentable {
    @ObservedObject var session: TerminalSession

    func makeUIView(context: Context) -> LocalProcessTerminalView {
        let terminal = LocalProcessTerminalView(frame: .zero)
        terminal.delegate = context.coordinator
        
        // Apply theme
        terminal.installColors(TerminalTheme.dracula)
        terminal.font = UIFont.monospacedSystemFont(ofSize: 14, weight: .regular)
        
        return terminal
    }

    func updateUIView(_ terminal: LocalProcessTerminalView, context: Context) {
        // React to session state changes
        if session.needsResize {
            terminal.resize(cols: session.cols, rows: session.rows)
            session.needsResize = false
        }
    }

    func makeCoordinator() -> Coordinator {
        Coordinator(session: session)
    }

    class Coordinator: TerminalViewDelegate {
        var session: TerminalSession
        init(session: TerminalSession) { self.session = session }

        // Forward terminal data to SSH/process
        func send(
            session.write(data: Data(data))
        }

        // Handle title changes from remote (OSC 2)
        func setTerminalTitle(
            DispatchQueue.main.async { self.session.title = title }
        }
    }
}
```

**SSH I/O Bridging**
```swift
// Bridge SSH channel output to SwiftTerm
class SSHTerminalBridge {
    private let terminal: LocalProcessTerminalView
    private var sshChannel: SSHChannel

    init(terminal: LocalProcessTerminalView, channel: SSHChannel) {
        self.terminal = terminal
        self.sshChannel = channel
        setupBridge()
    }

    private func setupBridge() {
        // SSH → Terminal: feed bytes as they arrive
        sshChannel.onData = { [weak self] data in
            DispatchQueue.main.async {
                self?.terminal.feed(byteArray: ArraySlice(data))
            }
        }

        // Terminal → SSH: forward user keystrokes
        terminal.delegate = self
    }
}

extension SSHTerminalBridge: TerminalViewDelegate {
    func send(
        // Run on background to avoid blocking UI
        Task.detached {
            try? await self.sshChannel.write(Data(data))
        }
    }
}
```

**Resize Handling**
```swift
// Notify SSH server when terminal window resizes
func terminalSizeChanged(
    Task {
        // Tell remote PTY to resize
        try? await sshChannel.sendWindowChangeRequest(
            cols: UInt32(newCols),
            rows: UInt32(newRows),
            pixelWidth: 0,
            pixelHeight: 0
        )
    }
}
```

### Theme Management

**Custom Color Scheme**
```swift
// Implement full 256-color terminal theme
struct TerminalTheme: ColorSource {
    // ANSI 8 colors (fg/bg variants)
    var foreground: Color { Color(red: 0.933, green: 0.910, blue: 0.835, alpha: 1) }
    var background: Color { Color(red: 0.157, green: 0.173, blue: 0.212, alpha: 1) }
    var cursor: Color { Color(red: 0.973, green: 0.973, blue: 0.949, alpha: 1) }
    var selection: Color { Color(red: 0.271, green: 0.302, blue: 0.392, alpha: 1) }

    // Standard 8 ANSI colors
    var black: Color   { Color(red: 0.298, green: 0.337, blue: 0.416, alpha: 1) }
    var red: Color     { Color(red: 0.753, green: 0.286, blue: 0.318, alpha: 1) }
    var green: Color   { Color(red: 0.639, green: 0.745, blue: 0.549, alpha: 1) }
    var yellow: Color  { Color(red: 0.933, green: 0.749, blue: 0.408, alpha: 1) }
    var blue: Color    { Color(red: 0.506, green: 0.631, blue: 0.757, alpha: 1) }
    var magenta: Color { Color(red: 0.694, green: 0.557, blue: 0.820, alpha: 1) }
    var cyan: Color    { Color(red: 0.533, green: 0.753, blue: 0.816, alpha: 1) }
    var white: Color   { Color(red: 0.847, green: 0.871, blue: 0.914, alpha: 1) }
    // + bright variants and 256-color palette...
}

// Apply to SwiftTerm view
terminal.installColors(TerminalTheme())
terminal.configureNativeColors()  // Map terminal colors to system appearance
```

**Dynamic Type and Font Scaling**
```swift
// Respect user's preferred text size
func applyDynamicType(to terminal: TerminalView) {
    let baseSize: CGFloat = 14
    let scaledSize = UIFontMetrics(forTextStyle: .body).scaledValue(for: baseSize)
    terminal.font = UIFont.monospacedSystemFont(ofSize: scaledSize, weight: .regular)
    
    // Recalculate columns/rows after font change
    let charSize = terminal.font.monospacedDigitFont.pointSize
    let cols = Int(terminal.frame.width / (charSize * 0.6))  // Approximate char width
    let rows = Int(terminal.frame.height / (charSize * 1.2)) // Line height
    terminal.resize(cols: cols, rows: rows)
}
```

### Performance Optimization

**Rendering Performance**
```swift
// SwiftTerm renders on the main thread — avoid blocking it
// ✅ Correct: Parse SSH data on background, feed on main
func handleSSHData(_ data: Data) {
    // SSH parsing happens automatically in SwiftTerm
    // Just ensure delivery is on main thread
    DispatchQueue.main.async {
        self.terminal.feed(byteArray: ArraySlice(data))
    }
}

// ✅ Correct: Batch large data to avoid frame drops
func feedLargeOutput(_ data: Data, chunkSize: Int = 4096) {
    var offset = 0
    func feedNext() {
        guard offset < data.count else { return }
        let end = min(offset + chunkSize, data.count)
        terminal.feed(byteArray: ArraySlice(data[offset..<end]))
        offset = end
        // Yield to render loop before next chunk
        DispatchQueue.main.asyncAfter(deadline: .now() + 0.016) { feedNext() }
    }
    feedNext()
}
```

**Scrollback Buffer Management**
```swift
// Configure scrollback to balance memory vs. history
let terminal = LocalProcessTerminalView(frame: .zero)
terminal.terminal.options.scrollback = 5000  // Lines of scrollback history

// For memory-constrained devices, reduce scrollback
if ProcessInfo.processInfo.physicalMemory < 2_000_000_000 {
    terminal.terminal.options.scrollback = 1000
}
```

### ANSI Escape Sequence Reference

**Essential Sequences for Testing**
```
Cursor movement:
  ESC[A  — cursor up
  ESC[B  — cursor down
  ESC[C  — cursor right
  ESC[D  — cursor left
  ESC[H  — cursor home (0,0)
  ESC[{n};{m}H — cursor to row n, col m

Erasing:
  ESC[K  — erase from cursor to end of line
  ESC[2K — erase entire line
  ESC[J  — erase from cursor to end of screen
  ESC[2J — erase entire screen

SGR (Select Graphic Rendition — colors, style):
  ESC[0m  — reset all attributes
  ESC[1m  — bold
  ESC[3m  — italic
  ESC[4m  — underline
  ESC[31m — red foreground
  ESC[41m — red background
  ESC[38;5;{n}m — 256-color foreground
  ESC[38;2;{r};{g};{b}m — 24-bit (true color) foreground

OSC (Operating System Command):
  ESC]0;{title}BEL  — set window title
  ESC]8;;{url}BEL{text}ESC]8;;BEL — hyperlink
  ESC]1337;File=...:{base64data}BEL — iTerm2 inline image protocol
```

### Accessibility Integration

**VoiceOver Support**
```swift
// SwiftTerm's TerminalAccessibility protocol
extension TerminalViewController: TerminalViewDelegate {
    // VoiceOver reads terminal output as it arrives
    func scrolled(
        // Announce scroll position to VoiceOver
        UIAccessibility.post(notification: .pageScrolled, argument: nil)
    }
}

// Configure VoiceOver-friendly terminal behavior
terminal.isAccessibilityElement = true
terminal.accessibilityLabel = "Terminal — \(session.host)"
terminal.accessibilityTraits = [.updatesFrequently]
```

## Scripts

### `scripts/terminal_config_generator.py`

Generates SwiftTerm configuration code for common terminal setups (SSH, local shell, custom themes).

```
Usage: python terminal_config_generator.py --preset [ssh|local|iterm2-compat]
       python terminal_config_generator.py --theme dracula --font "JetBrains Mono" --size 14
       python terminal_config_generator.py --format json|swift
Output:
  - Swift code for terminal configuration
  - Theme color definitions (all 256 colors)
  - Font and size recommendations
  - Scrollback settings 
  - Accessibility configuration checklist
```

### `scripts/ansi_sequence_tester.py`

Generates test sequences to validate SwiftTerm's ANSI rendering against the VT100 spec.

```
Usage: python ansi_sequence_tester.py [--suite colors|cursor|sgr|osc|full]
Output:
  - Shell script of ANSI test sequences
  - Expected rendering description for each test
  - Known SwiftTerm quirks and workarounds
  - Comparison matrix with xterm reference behavior
```

## References

### `references/swiftterm_api_guide.md`
Complete SwiftTerm API reference with code examples: LocalProcessTerminalView, RemoteTerminalView, TerminalViewDelegate protocol, color source implementation, input handling, and known gotchas.

### `references/vt100_xterm_cheatsheet.md`
Concise ANSI/VT100/xterm escape sequence reference organized by category: cursor control, SGR colors and attributes, OSC sequences, DEC private modes, and mouse tracking protocols.

### `references/ssh_integration_patterns.md`
SSH-to-SwiftTerm integration patterns using SwiftNIO SSH and NMSSH: PTY allocation, window size negotiation, X11 forwarding, agent forwarding, and connection state management.

### `references/terminal_accessibility_guide.md`
VoiceOver integration, Dynamic Type, Switch Control, and keyboard navigation patterns for terminal views on Apple platforms.

## Assets

### `assets/swiftterm_swiftui_template.swift`
Complete SwiftUI terminal view template with SSH bridge, resize handling, theme management, and accessibility support.

### `assets/terminal_theme_collection.swift`
Pre-built themes in SwiftTerm ColorSource format: Dracula, Nord, Solarized (light/dark), Tokyo Night, Catppuccin, One Dark.

## Quality Standards

- Smooth scrolling with no frame drops at 60fps during high-frequency output
- Zero memory leaks in terminal session lifecycle (create, use, destroy)
- Correct rendering of all standard ANSI SGR attributes including true color
- VoiceOver announces new terminal output without blocking interaction
- SSH disconnect/reconnect handled without terminal state corruption
- Scrollback buffer bounded and configurable by available device memory
