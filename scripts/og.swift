// Localised Open Graph images (1200×630 JPEG) from assets-src/og-base.jpg (the card made by the app repo's
// scripts/screenshot-og.swift: mascot, wordmark, phone). Repaints the text area with the same background gradient and
// draws the headline and the fact line again, so a fact (number of puzzles) or a language can change without the
// mascot render. build.py writes the lines into assets/og/manifest.json and warns when an image is out of date.
//
//   swiftc -O scripts/og.swift -o /tmp/zirve-og
//   /tmp/zirve-og ../zirve/App/Resources/Fonts assets/og/manifest.json
//
// Fredoka and Nunito come from the app repo (App/Resources/Fonts); Latin text only (CJK/Thai cards need other fonts).
import Foundation
import CoreGraphics
import CoreText
import ImageIO
import UniformTypeIdentifiers

let a = CommandLine.arguments
guard a.count >= 3 else { print("usage: og <fonts dir> <manifest.json>"); exit(1) }
let fontsDir = a[1], manifestPath = a[2]
let W: CGFloat = 1200, H: CGFloat = 630
let sRGB = CGColorSpace(name: CGColorSpace.sRGB)!
for name in ["Fredoka-VF.ttf", "Nunito-VF.ttf"] {
    CTFontManagerRegisterFontsForURL(URL(fileURLWithPath: "\(fontsDir)/\(name)") as CFURL, .process, nil)
}
func color(_ hex: String, _ alpha: CGFloat = 1) -> CGColor {
    var v: UInt64 = 0
    Scanner(string: String(hex.dropFirst())).scanHexInt64(&v)
    return CGColor(red: CGFloat((v >> 16) & 255) / 255, green: CGFloat((v >> 8) & 255) / 255, blue: CGFloat(v & 255) / 255, alpha: alpha)
}
func font(_ family: String, _ size: CGFloat, weight: Double) -> CTFont {
    let base = CTFontCreateWithName(family as CFString, size, nil)
    let desc = CTFontDescriptorCreateWithAttributes([kCTFontVariationAttribute: [2003265652: weight]] as CFDictionary)
    return CTFontCreateCopyWithAttributes(base, size, nil, desc)
}
let ink = "#1F2A24", ink2 = "#56655C", primary = "#2E7D5B"

struct Card: Codable { let file: String; let line1: String; let line2: String; let subline: String }
struct Manifest: Codable { let base: String; let cards: [Card] }
let manifest = try JSONDecoder().decode(Manifest.self, from: Data(contentsOf: URL(fileURLWithPath: manifestPath)))
let root = URL(fileURLWithPath: manifestPath).deletingLastPathComponent().deletingLastPathComponent().deletingLastPathComponent()
guard let src = CGImageSourceCreateWithURL(root.appendingPathComponent(manifest.base) as CFURL, nil),
      let base = CGImageSourceCreateImageAtIndex(src, 0, nil) else { fatalError("cannot read base image") }

for card in manifest.cards {
    let ctx = CGContext(data: nil, width: Int(W), height: Int(H), bitsPerComponent: 8, bytesPerRow: 0, space: sRGB,
                        bitmapInfo: CGImageAlphaInfo.premultipliedLast.rawValue)!
    ctx.draw(base, in: CGRect(x: 0, y: 0, width: W, height: H))
    ctx.translateBy(x: 0, y: H); ctx.scaleBy(x: 1, y: -1)   // top-left origin, as in screenshot-og.swift

    // Text area: x 60…755 keeps clear of the bottom-right blob (x ≥ 760); y 230…480 is below the top-left blob.
    ctx.saveGState()
    ctx.clip(to: CGRect(x: 60, y: 232, width: 695, height: 248))
    let g = CGGradient(colorsSpace: sRGB, colors: [color("#F6F9F3"), color("#EAF3E4"), color("#DCEAD3")] as CFArray, locations: [0, 0.55, 1])!
    ctx.drawLinearGradient(g, start: .zero, end: CGPoint(x: W, y: H * 0.6), options: [.drawsBeforeStartLocation, .drawsAfterEndLocation])
    ctx.restoreGState()

    func text(_ s: String, family: String, size: CGFloat, weight: Double, hex: String, x: CGFloat, baseline: CGFloat, maxWidth: CGFloat) {
        var pt = size
        var line: CTLine
        repeat {
            let attr = NSAttributedString(string: s, attributes: [
                NSAttributedString.Key(kCTFontAttributeName as String): font(family, pt, weight: weight),
                NSAttributedString.Key(kCTForegroundColorAttributeName as String): color(hex),
            ])
            line = CTLineCreateWithAttributedString(attr)
            pt *= 0.97
        } while CGFloat(CTLineGetTypographicBounds(line, nil, nil, nil)) > maxWidth && pt > size * 0.5
        ctx.saveGState()
        ctx.translateBy(x: x, y: baseline); ctx.scaleBy(x: 1, y: -1)
        ctx.textPosition = .zero
        CTLineDraw(line, ctx)
        ctx.restoreGState()
    }
    text(card.line1, family: "Fredoka", size: 74, weight: 650, hex: ink, x: 78, baseline: 302, maxWidth: 670)
    text(card.line2, family: "Fredoka", size: 74, weight: 650, hex: primary, x: 78, baseline: 386, maxWidth: 670)
    text(card.subline, family: "Nunito", size: 26, weight: 700, hex: ink2, x: 82, baseline: 452, maxWidth: 670)

    let flat = CGContext(data: nil, width: Int(W), height: Int(H), bitsPerComponent: 8, bytesPerRow: 0, space: sRGB,
                         bitmapInfo: CGImageAlphaInfo.noneSkipLast.rawValue)!
    flat.draw(ctx.makeImage()!, in: CGRect(x: 0, y: 0, width: W, height: H))
    let out = root.appendingPathComponent(card.file)
    let dest = CGImageDestinationCreateWithURL(out as CFURL, UTType.jpeg.identifier as CFString, 1, nil)!
    CGImageDestinationAddImage(dest, flat.makeImage()!, [kCGImageDestinationLossyCompressionQuality: 0.86] as CFDictionary)
    CGImageDestinationFinalize(dest)
    print("\(card.file) \(Int(W))×\(Int(H))")
}
// Record what was rendered: build.py uses a card only while it matches the current text (assets/og/rendered.json).
let encoder = JSONEncoder()
encoder.outputFormatting = [.prettyPrinted, .sortedKeys, .withoutEscapingSlashes]
try encoder.encode(manifest).write(to: root.appendingPathComponent("assets/og/rendered.json"))
