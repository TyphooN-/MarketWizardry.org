#!/usr/bin/env python3

import os
import subprocess

# Mapping of artist names to their respectful flavor text
FLAVOR_TEXT_MAP = {
    "0xDither": "0xDither's pixelated perfection where technical constraints become artistic revelation. Digital archaeology for collectors who understand that limitations breed creativity.",
    "0xEdwoods": "0xEdwoods's digital craftsmanship where precision meets personality. Methodical artistry for collectors who appreciate attention to algorithmic detail.",
    "1337skulls": "1337skulls's memento mori for the digital age where death meets decentralization. Gothic blockchain art for collectors who embrace beautiful mortality.",
    "5tr4n0": "5tr4n0's mysterious digital transmissions where signals become art. Cryptic creativity for collectors who appreciate encoded aesthetics.",
    "6taccc": "6taccc's systematic digital arrangements where order creates beauty. Structured artistry for collectors who find harmony in organized complexity.",
    "AINTNOTHINxart": "AINTNOTHINxart's raw digital authenticity where genuine expression cuts through algorithmic noise. Unfiltered creativity for collectors who value artistic honesty.",
    "ALCrego__": "ALCrego's alchemical digital transformations where base pixels become artistic gold. Transmutative art for collectors who appreciate creative chemistry.",
    "AcidSoupArt": "AcidSoupArt's psychedelic digital broth where consciousness dissolves into color. Mind-expanding visuals for collectors ready to experience reality differently.",
    "Bombadiluss": "Bombadiluss's whimsical digital adventures where playfulness meets profundity. Joyful artistry for collectors who appreciate when serious art doesn't take itself seriously.",
    "DarkenedM00d": "DarkenedM00d's melancholic digital poetry where darkness reveals light. Emotional depth for collectors who find beauty in digital introspection.",
    "FEELSxart": "FEELSxart's emotional digital landscapes where feelings become visible. Sentiment made tangible for collectors who appreciate when art wears its heart on its pixels.",
    "GenerativePunk": "GenerativePunk's algorithmic rebellion where code becomes counterculture. Digital punk rock for collectors who appreciate systematic anarchy.",
    "Gogolitus": "Gogolitus's theatrical digital performances where every pixel plays a role. Dramatic artistry for collectors who appreciate when technology takes the stage.",
    "GrantYun2": "Grant Yun's contemplative digital meditations where Eastern philosophy meets Western pixels. Balanced artistry for collectors seeking digital zen.",
    "HughesMichi": "Hughes Michi's architectural digital blueprints where structure becomes sculpture. Engineering artistry for collectors who appreciate when function follows beauty.",
    "Kirokaze": "Kirokaze's nostalgic digital memories where past and future collide in perfect pixels. Retro-futurism for collectors who appreciate temporal paradox.",
    "LexDoomArt": "Lex Doom's apocalyptic digital visions where endings become beginnings. Eschatological artistry for collectors who find hope in digital destruction.",
    "ManIcArt__": "ManIcArt's manic digital energy where intensity becomes artistry. Frenetic creativity for collectors who appreciate when art runs on pure adrenaline.",
    "MilaAugustova": "Mila Augustova's delicate digital botanics where nature grows in silicon soil. Organic digital art for collectors who appreciate when technology blooms.",
    "Micah_Alhadeff": "Micah Alhadeff's thoughtful digital compositions where contemplation creates beauty. Reflective artistry for collectors who appreciate meditative pixels.",
    "Nicolas_Sassoon": "Nicolas Sassoon's rhythmic digital waves where pattern becomes poetry. Hypnotic artistry for collectors who appreciate when repetition transcends monotony.",
    "PERFECTL00P": "PERFECTL00P's infinite digital cycles where endings are beginnings. Eternal artistry for collectors who appreciate when mathematics becomes mystical.",
    "XCOPYART": "XCOPY's glitched digital prophecies where malfunction becomes message. Corrupted beauty for collectors who understand that broken systems tell the best stories.",
    "Pho_Operator": "Pho Operator's culinary digital fusion where Eastern flavor meets Western pixels. Gastronomic art for collectors who appreciate when creativity is served hot.",
    "PierceLilholt": "Pierce Lilholt's penetrating digital insights where observation becomes art. Analytical creativity for collectors who appreciate when seeing becomes understanding.",
    "PlayStationPark": "PlayStation Park's nostalgic digital arcade where childhood memories level up. Gaming artistry for collectors who never stopped playing.",
    "Polygon1993": "Polygon1993's geometric digital archaeology where angular becomes emotional. Mathematical beauty for collectors who appreciate when shapes have souls.",
    "PunksDistorted": "Punks Distorted's rebellious digital static where corruption creates character. Glitch punk for collectors who appreciate beautiful imperfection.",
    "RJ16848519": "RJ16848519's coded digital identity where numbers become narrative. Algorithmic autobiography for collectors who appreciate when data tells human stories.",
    "RedruMxART": "RedruM Art's reversed digital psychology where backwards becomes forward. Mirror artistry for collectors who appreciate when reflection reveals truth.",
    "RemikzT": "RemikzT's reconstructed digital narratives where fragments form complete stories. Archaeological art for collectors who appreciate assembled beauty.",
    "RenatoxMarini": "Renato Marini's renaissance digital mastery where classical meets computational. Timeless artistry for collectors who appreciate when tradition teaches technology.",
    "RichardNadler1": "Richard Nadler's digital craftsmanship where precision meets passion. Artisanal pixels for collectors who appreciate handmade digital goods.",
    "YUDHO_XYZ": "YUDHO's dimensional digital experiments where reality gets optional. Spatial artistry for collectors who appreciate when up becomes down and pixels become portals.",
    "Zaharia_af": "Zaharia's analytical digital frameworks where logic becomes lyrical. Systematic beauty for collectors who appreciate when algorithms develop aesthetics.",
    "Zoen_calega": "Zoen Calega's zen digital minimalism where less becomes infinitely more. Meditative artistry for collectors who understand that emptiness contains everything.",
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
    "blac_ai": "blac ai's intelligent digital consciousness where artificial meets artistic. Machine learning beauty for collectors ready for the post-human aesthetic.",
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
    "natived_": "natived's indigenous digital wisdom where ancient knowledge meets modern pixels. Cultural bridge-building for collectors who appreciate when tradition teaches technology.",
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

def restore_gallery_from_git(artist_name):
    """Restore gallery from git and apply new features"""
    try:
        # Restore from working git commit
        subprocess.run([
            'git', 'checkout', 'e27f474', '--', f'nft-gallery/{artist_name}_gallery.html'
        ], cwd='/home/typhoon/git/MarketWizardry.org', check=True)
        
        # Update with new flavor text if available
        if artist_name in FLAVOR_TEXT_MAP:
            gallery_file = f'/home/typhoon/git/MarketWizardry.org/nft-gallery/{artist_name}_gallery.html'
            
            with open(gallery_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Replace flavor text - find the pattern and replace it
            import re
            pattern = r'(<div class="flavor-text">)[^<]*(</div>)'
            replacement = f'\\g<1>{FLAVOR_TEXT_MAP[artist_name]}\\g<2>'
            
            new_content = re.sub(pattern, replacement, content)
            
            with open(gallery_file, 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            print(f"Restored {artist_name}_gallery.html with new flavor text")
        else:
            print(f"Restored {artist_name}_gallery.html (no flavor text update available)")
        
        return True
        
    except subprocess.CalledProcessError:
        print(f"Could not restore {artist_name}_gallery.html from git")
        return False
    except Exception as e:
        print(f"Error restoring {artist_name}: {e}")
        return False

def main():
    """Restore all galleries from working git commit"""
    
    gallery_dir = "/home/typhoon/git/MarketWizardry.org/nft-gallery"
    
    updated_count = 0
    total_count = 0
    
    for filename in os.listdir(gallery_dir):
        if filename.endswith("_gallery.html") and filename != "all.html":  # Skip all.html as it's working
            artist_name = filename.replace("_gallery.html", "")
            total_count += 1
            
            if restore_gallery_from_git(artist_name):
                updated_count += 1
    
    print(f"\nCompleted: Restored {updated_count} out of {total_count} galleries from working git commit")

if __name__ == "__main__":
    main()