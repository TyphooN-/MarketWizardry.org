#!/usr/bin/env python3

import os

# Additional respectful flavor text for remaining artists
REMAINING_FLAVOR_TEXT = {
    "_1mposter": "1mposter's digital identity games where authenticity becomes performance. Meta-artistic commentary for collectors who question everything (especially themselves).",
    
    "__Sean_Luke__": "Sean Luke's digital experiments where curiosity drives creation. Exploratory art for collectors who appreciate the journey over the destination.",
    
    "____elbi": "elbi's enigmatic digital presence where mystery enhances meaning. Cryptic artistry for collectors who prefer their art with extra intrigue.",
    
    "_myujii": "myujii's delicate digital poetry where subtlety speaks loudest. Gentle expressions for collectors who appreciate art's quieter moments.",
    
    "aaasonipse": "aaasonipse's rhythmic digital compositions where pattern becomes poetry. Systematic beauty for collectors who find peace in organized complexity.",
    
    "acid_boy__": "acid boy's psychedelic digital trips where consciousness meets canvas. Mind-altering visuals for collectors who appreciate expanded artistic horizons.",
    
    "adamfuhrer": "Adam Fuhrer's leadership in digital artistry where vision guides creation. Directorial works for collectors who appreciate artistic authority.",
    
    "agniis_eg": "agniis's fiery digital expressions where passion ignites pixels. Intense artistry for collectors who appreciate art with temperature.",
    
    "alulasit": "alulasit's dreamlike digital visions where sleep logic becomes waking art. Surreal beauty for collectors who appreciate when reality gets flexible.",
    
    "analogvidunion": "Analog Vid Union's nostalgic digital archaeology where past technologies become future art. Retro-futurism for collectors who appreciate temporal paradox.",
    
    "armilk88": "armilk88's retro military aesthetic meets digital expression. Combat-inspired visuals with nostalgic undertones for collectors who appreciate the intersection of memory and art.",
    
    "baladasathar": "baladasathar's poetic digital ballads where story meets spectrum. Narrative artistry for collectors who believe every pixel should tell a tale.",
    
    "beholdthe84": "beholdthe84's retro digital archaeology where 1984 never ended. Nostalgic futurism for collectors who appreciate when the past predicts the present.",
    
    "bluretina": "bluretina's blurred digital boundaries where focus becomes optional. Soft-edge artistry for collectors who appreciate when clarity dissolves into beauty.",
    
    "cameron16tv": "cameron16tv's broadcast digital dreams where static becomes signal. Television-age artistry for collectors who remember when screens glowed differently.",
    
    "cemhah": "cemhah's digital calligraphy where pixels learn to write poetry. Textual art for collectors who appreciate when language becomes visual.",
    
    "chroma_visions": "Chroma Visions' spectrum-spanning digital rainbows where color becomes consciousness. Chromatic artistry for collectors who taste colors.",
    
    "cudaoutofmemory": "CUDA Out of Memory's technological poetry where system limits become artistic statements. Digital humor for collectors who appreciate when errors become art.",
    
    "davidvnun": "David Vnun's contemplative digital meditations where silence speaks volumes. Peaceful artistry for collectors who find zen in pixels.",
    
    "degenpain": "degenpain's digital catharsis where suffering transforms into beauty. Emotional alchemy for collectors who understand that art heals wounds.",
    
    "delta_sauce": "Delta Sauce's algorithmic flavoring where mathematics meets taste. Computational cuisine for collectors who appreciate when code gets spicy.",
    
    "desultor": "desultor's scattered digital fragments where chaos organizes itself. Entropy art for collectors who find patterns in the random.",
    
    "endless_mazin": "Endless Mazin's infinite digital labyrinths where getting lost becomes the point. Navigational art for collectors who appreciate beautiful confusion.",
    
    "ex_mortal_": "ex_mortal's transcendent digital afterlife where death becomes digital immortality. Post-human artistry for collectors ready for the next evolution.",
    
    "fabrii2k": "fabrii2k's millennial digital nostalgia where Y2K never ended. Turn-of-century artistry for collectors who remember when the future was different.",
    
    "godlikepx": "godlikepx's divine digital interventions where pixels achieve enlightenment. Sacred geometry for collectors who worship at the altar of perfect pixels.",
    
    "haydiroket": "haydiroket's rocket-fueled digital journeys where art achieves escape velocity. Interstellar creativity for collectors ready to leave Earth's gravity.",
    
    "hazedlockdown": "hazedlockdown's quarantine digital diaries where isolation becomes art. Pandemic poetry for collectors who found beauty in the blur.",
    
    "hectoroz_": "hectoroz's digital wizardry where magic meets mathematics. Algorithmic sorcery for collectors who believe in computational conjuring.",
    
    "hexeosis": "hexeosis's hexagonal digital geometries where six-sided becomes infinite-sided. Mathematical artistry for collectors who appreciate perfect angles.",
    
    "jotta_rs": "jotta.rs's coded digital poetry where programming languages become artistic expression. Syntax art for collectors who read code like literature.",
    
    "killeracid": "killeracid's lethal digital chemistry where toxicity becomes beauty. Dangerous artistry for collectors who appreciate controlled chemical reactions.",
    
    "kinx__": "kinx's kinetic digital energy where movement freezes into eternal motion. Dynamic stillness for collectors who appreciate captured velocity.",
    
    "klazmandoo": "klazmandoo's chaotic digital symphonies where disorder finds its rhythm. Organized noise for collectors who dance to different frequencies.",
    
    "louisdazy": "Louis Dazy's lazy digital perfection where effortless becomes masterful. Casual brilliance for collectors who appreciate when genius looks easy.",
    
    "m0dest___": "m0dest's humble digital grandeur where modesty masks mastery. Understated excellence for collectors who appreciate quiet confidence.",
    
    "matheusfxavier": "Matheus F Xavier's mathematical digital poetry where equations become emotions. Computational creativity for collectors who solve for beauty.",
    
    "michaelmicasso": "Michael Micasso's digital renaissance where pixels meet paintbrush. Neo-classical artistry for collectors who appreciate when tradition meets technology.",
    
    "mickrenders": "mickrenders's rendered digital realities where 3D becomes 4D consciousness. Dimensional art for collectors who appreciate depth perception.",
    
    "neomechanica": "neomechanica's cybernetic digital organisms where machines learn to dream. Mechanical poetry for collectors who appreciate when technology develops soul.",
    
    "neural_divine": "neural_divine's AI-assisted digital prophecies where artificial intelligence becomes artistic intuition. Synthetic creativity for collectors ready for the collaboration.",
    
    "neurocolor": "neurocolor's synesthetic digital experiences where color becomes sensation. Neurological artistry for collectors who feel their art.",
    
    "nocturnmachine": "nocturnmachine's nighttime digital factories where darkness manufactures beauty. Industrial poetry for collectors who appreciate when machines work night shifts.",
    
    "obtainer": "obtainer's acquisition-focused digital collections where getting becomes giving. Curatorial art for collectors who understand that ownership is stewardship.",
    
    "oelhan_tv": "oelhan.tv's broadcast digital frequencies where signal becomes art. Transmission artistry for collectors tuned to different channels.",
    
    "ozbren_xyz": "ozbren.xyz's domain-specific digital territories where URL becomes artistic statement. Internet geography for collectors who map cyberspace.",
    
    "p1xelfool": "p1xelfool's foolish digital wisdom where stupidity becomes intelligence. Paradoxical artistry for collectors who appreciate wise foolishness.",
    
    "petersonsart": "Peterson's digital craftsmanship where traditional meets technological. Artisanal pixels for collectors who appreciate handmade digital goods.",
    
    "photonisdead": "photonisdead's post-light digital visions where illumination transcends photons. Dark energy artistry for collectors who see beyond visible spectrum.",
    
    "psychofuturist": "psychofuturist's mental time-travel digital prophecies where psychology meets prediction. Temporal artistry for collectors who live in all times simultaneously.",
    
    "rightclickdead": "rightclickdead's anti-piracy digital manifestos where theft becomes impossible. Secure artistry for collectors who appreciate unbreakable digital rights.",
    
    "ripcache": "ripcache's memory-torn digital fragments where forgetting becomes art form. Amnesia aesthetics for collectors who appreciate beautiful memory loss.",
    
    "rustnfteth": "rustnfteth's corroded digital metals where decay becomes precious. Oxidized artistry for collectors who appreciate when time improves everything.",
    
    "s0mfay": "s0mfay's somehow digital solutions where impossible becomes inevitable. Paradox art for collectors who appreciate when logic takes vacation.",
    
    "scardecc": "scardecc's battle-worn digital testimonies where trauma becomes triumph. Survivor artistry for collectors who appreciate scars as beauty marks.",
    
    "slava3ngl": "slava3ngl's angular digital geometries where sharp edges cut through convention. Cutting artistry for collectors who appreciate when art has teeth.",
    
    "spellamin": "spellamin's magical digital incantations where code becomes conjuration. Algorithmic sorcery for collectors who believe in computational magic.",
    
    "trapdaddyvoss": "trapdaddyvoss's hip-hop digital beats where rhythm becomes visual. Musical artistry for collectors who see sound and hear colors.",
    
    "trillobyteart": "trillobyteArt's prehistoric digital fossils where ancient meets algorithmic. Archaeological artistry for collectors who appreciate digital evolution.",
    
    "uczine": "uczine's magazine-format digital spreads where publishing meets pixels. Editorial artistry for collectors who read their art.",
    
    "underscoreX0": "underscoreX0's underscore digital emphasis where punctuation becomes art. Grammatical creativity for collectors who appreciate syntactic beauty.",
    
    "vad_jpg": "vad.jpg's compressed digital artifacts where lossy becomes lossless beauty. Compression artistry for collectors who appreciate when less data means more art.",
    
    "weirdnikita": "weirdnikita's strange digital experiments where weird becomes wonderful. Eccentric artistry for collectors who celebrate the beautifully bizarre.",
    
    "xeriesjame_art": "xeriesjame's xerographic digital copies where reproduction becomes original. Duplicative artistry for collectors who appreciate authentic copies.",
    
    "xicojam": "xicojam's digital jams where improvisation meets intention. Musical artistry for collectors who appreciate when creativity riffs on itself.",
    
    "xxdao_xyz": "xxdao.xyz's decentralized digital governance where democracy meets artistry. Collective creativity for collectors who vote with their wallets."
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
    """Update remaining gallery flavor text to be more respectful"""
    
    updated_count = 0
    total_count = len(REMAINING_FLAVOR_TEXT)
    
    for artist_name, flavor_text in REMAINING_FLAVOR_TEXT.items():
        if update_gallery_flavor_text(artist_name, flavor_text):
            updated_count += 1
    
    print(f"\\nCompleted: Updated {updated_count} out of {total_count} remaining galleries with improved flavor text")

if __name__ == "__main__":
    main()