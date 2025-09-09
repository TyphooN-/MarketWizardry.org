#!/usr/bin/env python3

import os
import re

# Improved flavor text that's respectful but maintains dark humor in Sam Hyde style
IMPROVED_FLAVOR_TEXT = {
    "0xDither": "0xDither's pixelated perfection where technical constraints become artistic revelation. Digital archaeology for collectors who understand that limitations breed creativity.",
    
    "0xEdwoods": "0xEdwoods' haunted digital galleries where horror aesthetics meet artistic sophistication. Dark visual narratives for collectors brave enough to own beautiful nightmares.",
    
    "1337skulls": "1337skulls' memento mori collection where death imagery transcends into digital immortality. Skull aesthetics for collectors who appreciate the eternal dance between mortality and art.",
    
    "5tr4n0": "5tr4n0's corrupted digital landscapes where glitch becomes high art. Embracing digital entropy as aesthetic choice for collectors who see beauty in controlled chaos.",
    
    "6taccc": "6taccc's pixelated symphonies where digital noise becomes visual music. Structured complexity for collectors who appreciate the art of organized disorder.",
    
    "AINTNOTHINxart": "AINTNOTHINxart's minimalist statements where absence creates presence. Existential expressions for collectors who understand that void has substance.",
    
    "ALCrego_": "ALCrego's algorithmic poetry where code becomes canvas. Digital alchemy for collectors who appreciate when mathematics transcends into pure artistry.",
    
    "AcidSoupArt": "AcidSoupArt's psychedelic digital brew where reality bends into artistic vision. Mind-expanding visuals for collectors who appreciate consciousness as medium.",
    
    "Bombadiluss": "Bombadiluss's explosive visual experiments where destruction becomes creation. Dynamic digital energy for collectors who appreciate controlled creative detonation.",
    
    "DarkenedM00d": "DarkenedM00d's melancholic digital poetry where darkness reveals light. Emotional depth for collectors who find beauty in digital introspection.",
    
    "FEELSxart": "FEELSxart's emotional landscapes where feeling becomes form. Digital empathy for collectors who understand that art should make you feel something real.",
    
    "GenerativePunk": "GenerativePunk's algorithmic rebellion where code meets counterculture. Computational punk for collectors who appreciate when machines learn to misbehave.",
    
    "Gogolitus": "Gogolitus's surreal digital worlds where logic dissolves into pure imagination. Fantastical visions for collectors who prefer their reality slightly unhinged.",
    
    "GrantYun2": "GrantYun2's digital craftsmanship where pixels meet purpose. Refined artistry for collectors who appreciate meticulous attention to digital detail.",
    
    "HughesMichi": "HughesMichi's visual poetry where simplicity speaks volumes. Elegant statements for collectors who believe less can indeed be more.",
    
    "Kirokaze": "Kirokaze's pixel art mastery where retro meets renaissance. 8-bit sophistication for collectors who understand that constraints fuel creativity.",
    
    "LexDoomArt": "LexDoomArt's apocalyptic visions where digital doom becomes artistic bloom. Dark futures rendered beautifully for collectors who appreciate dystopian aesthetics.",
    
    "ManIcArt_": "ManIcArt's manic digital energy where intensity becomes artistry. High-voltage creativity for collectors who appreciate art at maximum amplitude.",
    
    "Micah_Alhadeff": "Micah Alhadeff's thoughtful compositions where digital meets deliberate. Contemplative works for collectors who appreciate artistic intention.",
    
    "MilaAugustova": "Mila Augustova's elegant digital expressions where grace meets pixels. Refined artistry for collectors who appreciate sophisticated digital beauty.",
    
    "Nicolas_Sassoon": "Nicolas Sassoon's digital environments where space becomes experience. Immersive worlds for collectors who appreciate when art becomes inhabitable.",
    
    "PERFECTL00P": "PERFECTL00P's infinite digital cycles where repetition becomes revelation. Hypnotic patterns for collectors who find zen in algorithmic meditation.",
    
    "Pho_Operator": "Pho Operator's digital experiments where technique meets vision. Innovative approaches for collectors who appreciate pushing pixels to their limits.",
    
    "PierceLilholt": "PierceLilholt's sharp digital aesthetics where precision meets artistic vision. Cutting-edge compositions for collectors who appreciate angular beauty and geometric rebellion.",
    
    "PlayStationPark": "PlayStationPark's nostalgic digital playgrounds where gaming culture becomes high art. Interactive memories for collectors who grew up with controllers in hand.",
    
    "Polygon1993": "Polygon1993's retro-futuristic visions where 90s aesthetics meet timeless appeal. Nostalgic perfection for collectors who remember when the future looked different.",
    
    "PunksDistorted": "PunksDistorted's rebellious digital mutations where punk ethos meets pixel art. Countercultural creativity for collectors who appreciate artistic anarchy.",
    
    "RJ16848519": "RJ16848519's mysterious digital signatures where anonymity becomes artistry. Enigmatic works for collectors who appreciate the poetry of the unknown.",
    
    "RedruMxART": "RedruMxART's bold digital statements where color bleeds into consciousness. Vivid expressions for collectors who believe art should assault your senses (in the best way).",
    
    "RemikzT": "RemikzT's digital landscapes where pixels paint impossible worlds. Fantastical environments for collectors who prefer their reality with extra imagination.",
    
    "RenatoxMarini": "Renato Marini's sophisticated digital compositions where technique serves vision. Masterful artistry for collectors who appreciate when skill meets soul.",
    
    "RichardNadler1": "Richard Nadler's contemplative digital works where thought becomes form. Intellectual artistry for collectors who appreciate art that makes you think.",
    
    "XCOPYART": "XCOPY's glitched digital prophecies where malfunction becomes message. Corrupted beauty for collectors who understand that broken systems tell the best stories.",
    
    "YUDHO_XYZ": "YUDHO's experimental digital frontiers where convention dissolves into innovation. Boundary-pushing art for collectors who appreciate the cutting edge of creativity.",
    
    "Zaharia_af": "Zaharia's digital symphonies where code composes visual music. Algorithmic artistry for collectors who hear colors and see sounds.",
    
    "Zoen_calega": "Zoen Calega's minimal digital statements where precision creates power. Clean artistry for collectors who appreciate the art of digital reduction."
}

def update_gallery_flavor_text(artist_name, new_flavor_text):
    """Update the flavor text in a gallery file"""
    gallery_file = f"/home/typhoon/git/MarketWizardry.org/nft-gallery/{artist_name}_gallery.html"
    
    if not os.path.exists(gallery_file):
        print(f"Gallery file not found: {gallery_file}")
        return False
    
    with open(gallery_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find the flavor text section and replace it
    start_tag = '<div class="flavor-text">'
    end_tag = '</div>'
    
    start_index = content.find(start_tag)
    if start_index == -1:
        print(f"No flavor text found in {artist_name}")
        return False
    
    start_content = start_index + len(start_tag)
    end_index = content.find(end_tag, start_content)
    
    if end_index == -1:
        print(f"Malformed flavor text in {artist_name}")
        return False
    
    # Replace the content between the tags
    new_content = content[:start_content] + new_flavor_text + content[end_index:]
    
    if new_content != content:
        with open(gallery_file, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Updated flavor text for {artist_name}")
        return True
    else:
        print(f"No changes needed for {artist_name}")
        return False

def main():
    """Update gallery flavor text to be more respectful"""
    
    updated_count = 0
    total_count = len(IMPROVED_FLAVOR_TEXT)
    
    for artist_name, flavor_text in IMPROVED_FLAVOR_TEXT.items():
        if update_gallery_flavor_text(artist_name, flavor_text):
            updated_count += 1
    
    print(f"\\nCompleted: Updated {updated_count} out of {total_count} galleries with improved flavor text")

if __name__ == "__main__":
    main()