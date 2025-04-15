# game_script.rpy

# Basic Ren'Py configuration
# define config.developer = True

define balance = 1000

define e = Character("Elysia", color="#c8ffc8")
define p = Character("Police", color="#c8c8ff")
define dk = Character("Desert King", color="#ffc8c8")
define s = Character("Sorren", color="#c8c8ff")
define r = Character("Raven", color="#ffc8c8")
define pkr = Character("Opponent", color="#ffc8c8")
define bar = Character("Bartender", color="#c8c8ff")

# Elysia
image elysia = "images/sprites/sf1_outfit1_normal.png"
image elysia_talk = "images/sprites/sf1_outfit1_normaltalk.png"
image elysia_huh = "images/sprites/sf1_outfit1_huh.png"
image elysia_cry = "images/sprites/sf1_outfit1_cry.png"
image elysia_angry = "images/sprites/sf1_outfit1_angry.png"
image elysia_angrytalk = "images/sprites/sf1_outfit1_angrytalk.png"
image elysia_umm = "images/sprites/sf1_outfit1_umm.png"

# Police
image police = "images/sprites/sm1_sensei_normal.png"
image police_smile = "images/sprites/sm1_sensei_smile.png"
image police_pout = "images/sprites/sm1_sensei_pout.png"
image police_talk = "images/sprites/sm1_sensei_talk.png"

# Desert Kings
image dk = "images/sprites/ssn_sports_normal.png"
image dk_angry = "images/sprites/ssn_sports_angry.png"
image dk_angrytalk = "images/sprites/ssn_sports_angrytalk.png"
image dk_angrylaugh = "images/sprites/ssn_sports_angrylaugh.png"

# councilwoman
image sorren = "images/sprites/sf2g_sensei_normal.png"
image sorren_talk = "images/sprites/sf2g_sensei_normaltalk.png"

# raven cross
image raven = "images/sprites/haruo_butler_normal.png"
image raven_talk = "images/sprites/haruo_butler_normaltalk.png"
image raven_smirk = "images/sprites/haruo_butler_smirk.png"

init python:
    # Function to update the player's balance
    def update_balance(amount):
        global balance
        balance += amount
        SetVariable("balance", balance)()

# The start label is where the game begins.
label start:
    play music "431_Hotel_Noir.mp3"
    scene lights with fade
    show screen stats_screen

    "Las Vegas – bright neon, glittering casinos, and endless entertainment. Yet here, prostitution is officially illegal."
    show elysia at center with dissolve
    "Your name is Elysia, a sex worker navigating a secret world hidden beneath the city lights."

    hide elysia
    show elysia_talk at center
    e "{i}It was business doing pleasure with you! Have a good night!{/i}"

    $ payment = renpy.random.randint(500, 1000)
    $ update_balance(payment)
    "You just finished a job with a discreet client, earning $[payment]. Not bad!"

    hide elysia_talk
    show elysia_huh at center
    "But the night is still young, and the city is full of opportunities... or dangers."

    menu:
        "What do you do?"
        "Go straight home":
            jump go_home
        "Visit the Majestic Spire Casino":
            jump casino_detour

label go_home:
    show elysia at center with dissolve
    "You decide to return home and avoid potential trouble. The streets are quiet, but vice squads roam. One misstep could end in arrest..."
    jump act1

label casino_detour:
    play music "273_Arcane_Clockworks.mp3"
    scene casino_interior with dissolve
    show elysia at center with dissolve
    "You head to the Majestic Spire Casino, a lavish hotspot. The machines beep, chips rattle, and high-rollers bustle."
    "You can either partake in casino games or grab a drink at the bar."

    menu:
        "What do you do?"
        "Play poker (risky)":
            jump casino_floor
        "Grab a drink (safe)":
            jump casino_drink

label casino_floor:
    scene casino_floor with dissolve
    show elysia at center with dissolve
    "You sit at a poker table, eyeing the players. The stakes are high, and the atmosphere is electric."
    
    $ buy_in = renpy.random.randint(100, 500)
    $ update_balance(-buy_in)  # Deduct buy-in from balance
    
    "You buy in for $[buy_in], and the dealer slides you a stack of chips."
    "The next hand begins, and you peel back an ace of spades and an ace of clubs."
    e "{i}Ooh, pocket aces. I raise.{/i}"
    pkr "{i}I call.{/i}"
    "The flop is a rainbow: 3 of hearts, 5 of diamonds, and 9 of clubs."
    e "{i}Looks safe. I bet.{/i}"
    pkr "{i}Eh, I call.{/i}"
    "The dealer flips the turn card, and it's a heart."
    e "{i}Still no danger. Lets put more chips in.{/i}"
    pkr "{i}Sure, why not?{/i}"
    "The dealer reveals the river card, a 10 of hearts."
    hide elysia
    show elysia_huh at center
    e "{i}Hmm. My aces are strong, but I'm worried about a flush. I'll check.{/i}"
    pkr "{i}ALL IN.{/i}"
    hide elysia_huh
    show elysia_umm at center
    e "{i}Shoot. I was hoping he didn't do that. Now I have to decide if he has the nuts or is bluffing.{/i}"
    
    menu:
        "What's your move?"

        "Call—he's bluffing!":
            e "{i}You're bluffing! I call.{/i}"
            hide elysia_umm
            $ win_chance = renpy.random.randint(1, 2)
            if win_chance == 1:
                show elysia_talk at center
                pkr "{i}Good hand. I fold.{/i}"
                e "{i}Let's go!{/i}"
                $ winnings = buy_in * 2  # Double the buy-in
                $ update_balance(winnings)  # Update balance with winnings
                "You gain $[winnings]."
            else:
                show elysia_cry at center
                pkr "{i}Nice try, but I have a flush.{/i}"
                e "{i}Ugh, I should have folded.{/i}"
                "You lose your buy-in of $[buy_in]."
        
        "Fold—he's got the nuts!":
            $ lost = int(buy_in * 0.5)  # Assume you lose half your buy-in for folding
            $ remaining = buy_in - lost  # Remaining balance after folding
            $ update_balance(remaining)  # Update balance with loss
            e "{i}I'm not risking it. I fold.{/i}"
            "You leave the table with your remaining chips—$[remaining]."

    hide elysia_umm
    show elysia_huh at center

    show police at left with dissolve
    "Suddenly, you spot a vice cop in plain clothes. You need to act fast!"
    menu:
        "What do you do?"
        "Try to blend in":
            hide elysia_huh
            show elysia at center
            "You attempt to act natural, but the cop's gaze lingers on you."
            hide police
            show police_pout at left
            "You manage to slip away unnoticed. That was close!"
        
        "Confront the cop":
            hide elysia_huh
            hide police
            show police_talk at left
            "You decide to confront the cop, thinking you can talk your way out."
            $ confront_chance = renpy.random.randint(1, 2)
            if confront_chance == 1:
                show elysia_angrytalk at center
                e "{i}What are you looking at?{/i}"
                p "{i}Just doing my job. What's your business here?{/i}"
                e "{i}Uh, just enjoying the casino. No harm done.{/i}"
                hide police_talk
                show police_pout at left
                p "{i}They why are you dressed like that? Let's see your ID.{/i}"
                p "{i}Elysia, right? I know you. You're on the list. You're coming with me.{/i}"
                jump gameover_arrest
            else:
                show elysia_talk at center
                e "{i}What's the problem, officer?{/i}"
                p "{i}Just checking in. You know how it is.{/i}"
                e "{i}Yeah, I know. Just trying to have a good time.{/i}"
                p "{i}Sure, but keep it low-key.{/i}"
                "Your boldness pays off. The cop backs off, and you escape."

    jump act1

label casino_drink:
    scene casino_bar with dissolve
    show elysia_talk at center with dissolve

    "You choose to quietly sit at the casino bar."
    e "{i}I'll take the house special.{/i}"
    bar "{i}Coming right up!{/i}"

    $ drink_cost = renpy.random.randint(5, 25)
    $ update_balance(-drink_cost)  # Cost of the drink
    "The drink costs you $[drink_cost]. You enjoy the ambiance, but the night is still young."
    jump act1

# Act I: Life Under Prohibition
label act1:
    play music "32_City_and_the_City.mp3"
    scene street_night with fade
    "Despite any side ventures, the fact remains: Prostitution is illegal here."
    show police at left with dissolve
    show dk_angry at right with dissolve
    "Vice squads conduct stings in popular areas, while the Desert Kings gang demands 'protection fees' from workers on their turf."
    "You hear about a moralist group, Pure Vegas, calling for even harsher crackdowns."

    menu:
        "Choose your next action under prohibition:"
        "Operate in usual spots (risky)":
            jump act1_risky
        "Pay for safer hideouts":
            jump act1_safe

label act1_risky:
    "You stick to familiar areas, trying to maintain your income."
    $ arrest_chance = renpy.random.randint(1, 2)
    if arrest_chance == 1:
        jump gameover_arrest
    else:
        "Somehow, you avoid undercover officers for now. But tensions rise each night."

        $ payment = renpy.random.randint(300, 700)
        $ update_balance(payment)
        "You earn $[payment] from your usual spots. But the risk is visible."

        jump desert_kings

label act1_safe:
    $ payment = renpy.random.randint(200, 500)
    $ update_balance(-payment)  # Deduct payment for safer hideouts

    "You invest $[payment] in hush-hush meeting places, reducing the chance of a sting."
    "Your earnings drop, but you gain relative safety."
    jump desert_kings

label desert_kings:
    scene alley_dark with fade
    show dk_angrytalk at center with dissolve

    "Oh no! The Desert Kings are here!"
    dk "{i}Hey, darling. Having a good night?{/i}"
    e "{i}Uh, yeah. Just... working.{/i}"
    dk "{i}Well, you know the drill. We keep you safe from the cops, and you give us a cut. How's that sound?{/i}"

    menu:
        "Do you pay the Desert Kings?"
        "Pay the fee":
            jump desert_pay
        "Refuse":
            jump desert_refuse

label desert_pay:
    $ payment = renpy.random.randint(100, 300)
    $ update_balance(-payment)  # Deduct payment for the gang

    hide dk_angrytalk
    show dk at center
    "You reach into your pocket and hand over $[payment]."
    e "{i}Fine, just take it.{/i}"
    dk "{i}Good girl. I know you'll come around. Just keep your head down, and we won't have any problems.{/i}"
    "The Desert Kings leave you alone for now, but you know they'll be back."

    hide dk with dissolve

    show elysia_talk at center with dissolve
    "Shortly after, you befriend Leena, a veteran sex worker who helps you dodge vice cops."
    hide elysia_talk
    show elysia_huh at center
    "Meanwhile, Pure Vegas intensifies raids in your area..."
    jump act1_backlash

label desert_refuse:
    e "{i}No way. I'm not paying you anything.{/i}"
    hide dk_angrytalk
    show dk_angry at center
    dk "{i}Oh, really? You think you can just walk away?{/i}"
    $ gang_attack = 1
    if gang_attack == 1:
        "You make a run for it, but the Desert Kings are quick."
        jump gameover_assault
    else:
        "Somehow, you slip under the gang's radar—for now. You meet Leena, who shows you ways to avoid cops."
        jump act1_backlash

label act1_backlash:
    "Pure Vegas organizes moral campaigns, resulting in bigger crackdowns. One raid nearly catches you and Leena."
    "You narrowly evade a sting. Unfortunately, Leena gets arrested in the process. You proceed alone."
    jump act2

# Act II: Seeds of Change
label act2:
    play music "131_The_Bog_Standard.mp3"
    scene city_council with fade
    show sorren_talk at center with dissolve
    "Public concern grows as arrests multiply. People see the ban fueling exploitation. Councilwoman Sorren proposes legalizing prostitution with strict regulations."
    s "{i}We need to protect workers and ensure safety. Legalization is the way forward.{/i}"
    menu:
        "You hear about a secret activist meeting for sex workers."
        "Attend the meeting":
            jump activism_meeting
        "Stay low":
            jump activism_avoid

label activism_meeting:
    hide sorren_talk with dissolve
    show elysia_talk at center with dissolve
    "You meet other workers and social advocates. They support Sorren's bill, sharing hopes for safety and fair treatment."
    jump legal_debates

label activism_avoid:
    hide sorren_talk with dissolve
    show elysia_huh at center with dissolve
    "You skip the meeting, wary of attention. You stay alone with your worries."
    jump legal_debates

label legal_debates:
    "Sorren's proposal sparks fierce opposition from Pure Vegas."
    show dk_angry at right with dissolve
    "Meanwhile, the Desert Kings try to sabotage the bill to keep their black-market control."
    menu:
        "A City Council hearing invites public testimony."
        "Testify":
            hide dk_angry with dissolve
            hide elysia_huh
            jump testify_scene
        "Remain silent":
            hide dk_angry with dissolve
            hide elysia_huh
            jump silent_scene

label testify_scene:
    show elysia_umm at center
    "Nervously, you speak of the dangers you face daily. You might sway some council members."
    $ sabotage_chance = renpy.random.randint(1, 3)
    if sabotage_chance == 1:
        "Unfortunately, the Desert Kings hear about your testimony. They are not happy."
        jump gameover_assault
    else:
        hide elysia_umm
        show elysia_talk at center
        "Despite potential threats, you finish your testimony safely."
        $ reward = renpy.random.randint(500, 1000)
        $ update_balance(reward)  # Update balance with reward
        "You earn $[reward] for your bravery."
        jump narrow_victory

label silent_scene:
    show elysia at center
    "You skip the hearing, avoiding potential risks. Your voice is unheard, though your safety remains intact."
    jump narrow_victory

label narrow_victory:
    "After an intense debate, the council narrowly legalizes prostitution in Las Vegas under strict licensing and health regulations."
    "Pure Vegas protests, but for now, you see a glimmer of hope."
    jump act3

# Act III: The Legalized Future
label act3:
    play music "32_City_and_the_City.mp3"
    scene city_legal with fade
    show elysia at center with dissolve
    "With the new law in effect, you officially register as a sex worker. A Workers' Cooperative forms to provide safer sites, medical access, and legal support."
    "Still, issues linger—social stigma, new fees, and possible under-the-table threats from the Desert Kings."
    menu:
        "Do you join the co-op or remain solo?"
        "Join the co-op":
            jump coop_join
        "Stay independent":
            jump coop_solo

label coop_join:
    $ payment = renpy.random.randint(100, 300)
    $ update_balance(-payment)  # Deduct payment for joining the co-op

    hide elysia
    show elysia_talk at center

    "You join the cooperative, paying $[payment] in dues. You gain access to safer workspaces and legal support."

    $ earnings = renpy.random.randint(200, 500)
    $ update_balance(earnings)  # Update balance with earnings
    "Bam! You earn $[earnings] for your first job through the co-op. The work is safer, and you feel more secure."

    "You also meet Leena again, who is now a co-op leader. She offers you a chance to help organize the new system."
    jump continuing_challenges

label coop_solo:
    "You choose not to pay co-op dues, preferring independence. You have more freedom but less fallback if trouble arises."
    jump continuing_challenges

label continuing_challenges:
    "Pure Vegas still organizes protests outside legalized workplaces."
    "The new casino manager, Raven Cross, proposes a VIP lounge for high-rollers seeking \"entertainment\" and asks for your input."
    "You also hear about a missing coworker, Ava."

    menu:
        "What do you want to do?"
        "Talk to Raven about the VIP lounge":
            jump vip_lounge
        "Investigate the missing worker":
            jump missing_worker

label vip_lounge:
    play music "273_Arcane_Clockworks.mp3"
    scene casino_vip with dissolve
    show raven_talk at center with dissolve

    r "{i}Thanks for coming, Elysia.{/i}"
    e "{i}No problem. What's up?{/i}"
    r "{i}Ever since the legalization, we've seen a surge in demand for high-end services.{/i}"
    r "{i}I want to create a VIP lounge for high-rollers. It'll be exclusive, luxurious, and... well, you know what I mean.{/i}"
    e "{i}Sounds intriguing. What's in it for me?{/i}"
    r "{i}A cut of the profits, of course. Plus, you'll be part of something big. What say you?{/i}"

    "You can either negotiate for better working conditions or rush the deal for quick profit."

    menu:
        "Negotiate or rush?"
        "Negotiate worker protections":
            hide raven_talk
            show raven at center
            e "{i}I think we should ensure fair wages and safety for everyone involved.{/i}"
            r "{i}Okay. I'm sure we can work something out.{/i}"
            hide raven with dissolve
            show elysia at center with dissolve
            "You gain allies and a solid reputation, but the Desert Kings may retaliate."
            $ negotiate_chance = renpy.random.randint(1, 3)
            if negotiate_chance == 2:
                jump gameover_assault
            else:
                hide elysia
                show elysia_talk at center
                "You successfully negotiate better working conditions and a fair cut of the profits."
                $ payment = renpy.random.randint(500, 1000)
                $ update_balance(payment)  # Update balance with payment
                "You earn $[payment] for your efforts."
                "You are now a respected figure in the co-op, and your actions inspire others."
        
        "Rush the deal":
            hide raven_talk
            show raven_smirk at center
            e "{i}I'm in. Let's do this.{/i}"
            r "{i}Just what I wanted to hear.{/i}"
            hide raven_smirk with dissolve
            show elysia_umm at center with dissolve
            "If conflict goes too far, you might be blamed. In extreme chaos, you could face legal repercussions or violence from outraged coworkers."
            $ rush_chance = renpy.random.randint(1, 4)
            if rush_chance == 1:
                jump gameover_arrest
            else:
                hide elysia_umm
                show elysia_huh at center
                "You manage to escape the chaos, but your reputation suffers. You lose allies and face a backlash from the co-op."

                $ payment = renpy.random.randint(300, 700)
                $ update_balance(payment)  # Update balance with payment

                "You earn $[payment] for your quick decision."
        
    jump new_opportunities

label missing_worker:
    play music "32_City_and_the_City.mp3"
    scene alley_dark with dissolve
    show elysia_huh at center with dissolve
    "A co-op member named Ava mysteriously disappeared."
    show dk_angry at right with dissolve
    "Rumor says the Desert Kings kidnapped her for disobeying them."
    menu:
        "Investigate or ignore?"
        "Investigate":
            hide elysia_huh
            show elysia_umm at center
            "You and a few allies try to rescue Ava. This is dangerous: the gang may ambush you."
            $ rescue_chance = renpy.random.randint(1, 2)
            if rescue_chance == 1:
                jump gameover_assault
            else:
                hide elysia_umm
                show elysia_talk at center
                "You succeed, freeing Ava. Your heroic act wins major respect within the co-op."

                $ payment = renpy.random.randint(500, 1000)
                $ update_balance(payment)  # Update balance with payment

                "Out of gratitude, Ava gives you $[payment]."

                jump new_opportunities

        "Ignore":
            "You decide to stay out of it. You don't want to risk your safety."
            jump new_opportunities

label new_opportunities:
    play music "431_Hotel_Noir.mp3"
    scene future_work with dissolve
    show elysia at right with dissolve
    "With legalized sex work, authorities now focus on genuine trafficking."
    "The Desert Kings lose their foothold on forced labor or intimidation. You feel a fresh breeze of safety."
    "Yet you must decide your personal path:"
    menu:
        "Continue sex work or move on?"
        "Stay in the industry":
            jump ending_stay
        "Seek a different career":
            jump ending_move_on

label ending_stay:
    play music "32_City_and_the_City.mp3"
    scene street_night with fade
    show elysia at center with dissolve
    "You settle into your newly regulated profession, forging a stable future under legal protections."
    hide elysia
    show elysia_talk at center
    "You become a key figure in the shifting landscape of Las Vegas sex work."
    "The End."
    jump end_screen

label ending_move_on:
    play music "131_The_Bog_Standard.mp3"
    scene hospitality with fade
    show elysia at center with dissolve
    "You use your earnings, experience, and newly found stability to transition into a different line of work."
    hide elysia
    show elysia_talk at center
    "You find a job in the hospitality industry, using your skills to help others and leave sex work behind on your own terms."
    "The End."
    jump end_screen

# Game Over Scenes
label gameover_arrest:
    play music "siren.mp3" noloop
    scene busted with dissolve
    show elysia_angry at left with dissolve
    show police_smile at right with dissolve
    "Busted! Vice cops catch you in a sting operation. You are arrested and face charges."
    
    $ balance = 0  # Reset balance to zero on game over

    "You are fined for the rest of your earnings, and your reputation is tarnished."
    "GAME OVER."
    jump end_screen

label gameover_assault:
    scene assault with dissolve
    play music "moan.mp3" noloop

    $ balance = 0  # Reset balance to zero on game over

    show elysia_cry at left with dissolve
    show dk_angrylaugh at right with dissolve

    "Violence strikes. The Desert Kings catch up with you. You can't escape the assault."
    "GAME OVER."
    jump end_screen

label end_screen:
    play music "273_Arcane_Clockworks.mp3"
    hide screen stats_screen
    scene black with fade

    if balance > 3000:
        show elysia_talk at center with dissolve
        "Final balance: $[balance]\nCongratulations! You made a fortune!"
    elif balance > 2000:
        show elysia_talk at center with dissolve
        "Final balance: $[balance]\nWell done! That's a decent profit!"
    elif balance > 1000:
        show elysia at center with dissolve
        "Final balance: $[balance]\nNot bad! You did well."
    elif balance > 500:
        show elysia at center with dissolve
        "Final balance: $[balance]\nYou made it through, but there's room for improvement."
    elif balance > 1:
        show elysia_cry at center with dissolve
        "Final balance: $[balance]\nYou survived... barely."
    else:
        show elysia_cry at center with dissolve
        "Final balance: $[balance]\nYou lost everything. Better luck next time!"

    return
