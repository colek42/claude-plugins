// Mirror the laptop display onto the teleprompter so the call sits behind the camera.
// The teleprompter is any online display that is neither built-in nor the ultrawide.
//   teleprompter        mirror the laptop onto it
//   teleprompter off    stop mirroring
//   teleprompter list   show displays
import CoreGraphics
import Foundation

let ultrawideWidth = 5120

func online() -> [CGDirectDisplayID] {
    var n: UInt32 = 0
    CGGetOnlineDisplayList(0, nil, &n)
    var ids = [CGDirectDisplayID](repeating: 0, count: Int(n))
    CGGetOnlineDisplayList(n, &ids, &n)
    return ids
}

let displays = online()
let builtin = displays.first { CGDisplayIsBuiltin($0) != 0 }
let prompter = displays.first { CGDisplayIsBuiltin($0) == 0 && CGDisplayPixelsWide($0) != ultrawideWidth }
let arg = CommandLine.arguments.dropFirst().first ?? ""

if arg == "list" {
    for d in displays {
        let role = CGDisplayIsBuiltin(d) != 0 ? "built-in" : d == prompter ? "teleprompter" : "ultrawide"
        print("\(d) \(CGDisplayPixelsWide(d))x\(CGDisplayPixelsHigh(d)) \(role) mirrorOf=\(CGDisplayMirrorsDisplay(d))")
    }
    exit(0)
}
guard let builtin, let prompter else {
    print("no teleprompter display found (\(displays.count) online)")
    exit(1)
}
var cfg: CGDisplayConfigRef?
CGBeginDisplayConfiguration(&cfg)
let err = CGConfigureDisplayMirrorOfDisplay(cfg, prompter, arg == "off" ? kCGNullDirectDisplay : builtin)
let done = CGCompleteDisplayConfiguration(cfg, .permanently)
print(err == .success && done == .success ? (arg == "off" ? "mirroring off" : "laptop mirrored to teleprompter \(prompter)") : "failed: \(err.rawValue) \(done.rawValue)")
exit(err == .success && done == .success ? 0 : 1)
