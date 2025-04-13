# game_script.rpy

# Basic Ren'Py configuration
# define config.developer = True

define balance = 1000

# Elysia
image elysia = 'images/sprites/sf1_outfit1_normal.png'
image elysia_talk = 'images/sprites/sf1_outfit1_normaltalk.png'
image elysia_huh = 'images/sprites/sf1_outfit1_huh.png'
image elysia_cry = 'images/sprites/sf1_outfit1_cry.png'
image elysia_angry = 'images/sprites/sf1_outfit1_angry.png'
image elysia_angrytalk = 'images/sprites/sf1_outfit1_angrytalk.png'
image elysia_umm = 'images/sprites/sf1_outfit1_umm.png'

# Police
image police = 'images/sprites/sm1_sensei_normal.png'
image police_smile = 'images/sprites/sm1_sensei_smile.png'
image police_pout = 'images/sprites/sm1_sensei_pout.png'
image police_talk = 'images/sprites/sm1_sensei_talk.png'

# Desert Kings
image dk = 'images/sprites/ssn_sports_normal.png'
image dk_angry = 'images/sprites/ssn_sports_angry.png'
image dk_angrytalk = 'images/sprites/ssn_sports_angrytalk.png'

# councilwoman
image sorren = 'images/sprites/sf2g_sensei_normal.png'
image sorren_talk = 'images/sprites/sf2g_sensei_normaltalk.png'

# raven cross
image raven = 'images/sprites/haruo_butler_normal.png'
image raven_talk = 'images/sprites/haruo_butler_normaltalk.png'
image raven_smirk = 'images/sprites/haruo_butler_smirk.png'

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

    # Introduction
    "Las Vegas – bright neon, glittering casinos, and endless entertainment. Yet here, prostitution is officially illegal."
    show elysia at center with dissolve
    "Your name is Elysia, a sex worker navigating a secret world hidden beneath the city lights."

    # Initial payment for the first job
    $ payment = renpy.random.randint(500, 1000)
    $ update_balance(payment)

    hide elysia
    show elysia_talk at center
    "You just finished a job with a discreet client, earning $[payment]. Not bad!"

    hide elysia_talk
    show elysia_huh at center
    "But the night is still young, and the city is full of opportunities... or dangers."

    # First decision: go home or visit the casino
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
    "The next hand begins, and you peel back an ace of spades and an ace of clubs—pocket aces!"
    "Naturally, you play aggressively, raising the stakes."
    "The flop is a rainbow: 3 of hearts, 5 of diamonds, and 9 of clubs. Looks safe. You bet again."
    "The opponent calls, and the pot grows."
    "The dealer flips the turn card, and it's a heart. Still no danger. You bet again."
    "The opponent calls."
    "The river card is a 10 of hearts. You have a strong hand, but you're concerned that your opponent might have a flush which beats your aces."
    "You check, hoping your opponent will follow suit."
    hide elysia
    show elysia_huh at center
    "Unfortunately, he goes all-in."
    hide elysia_huh
    show elysia_umm at center
    
    menu:
        "You have a tough decision to make. Do you think he has the nuts, or is he just bluffing?"

        "Call—he's bluffing!":
            "You call and flip over your aces."
            hide elysia_umm
            # 50% chance of winning or losing
            $ win_chance = renpy.random.randint(1, 2)
            if win_chance == 1:
                show elysia_talk at center
                "The opponent flips a 2 and a 7. You win the hand!"
                $ winnings = buy_in * 2  # Double the buy-in
                $ update_balance(winnings)  # Update balance with winnings
                "You gain $[winnings]."
            else:
                show elysia_cry at center
                "The opponent shows a flush and your heart sinks."
                "You lose your buy-in of $[buy_in]."
        
        "Fold—he's got the nuts!":
            $ lost = int(buy_in * 0.5)  # Assume you lose half your buy-in for folding
            $ remaining = buy_in - lost  # Remaining balance after folding
            $ update_balance(remaining)  # Update balance with loss
            "You fold, deciding to play it safe. You leave the table with your remaining chips—$[remaining]."

    hide elysia_umm
    show elysia_huh at center

    # 50% chance of immediate bust, as an example
    $ chance_encounter = renpy.random.randint(1, 2)
    if chance_encounter == 1:
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
                show elysia_angrytalk at center
                show police_talk at left
                "You decide to confront the cop, thinking you can talk your way out."
                # 50% chance of being caught
                $ confront_chance = renpy.random.randint(1, 2)
                if confront_chance == 1:
                    jump gameover_arrest
                else:
                    hide elysia_angrytalk
                    show elysia_talk at center
                    "Your boldness pays off. The cop backs off, and you escape."
    else:
        hide elysia_huh
        show elysia at center
        "You manage to keep your head low and avoid trouble, for now."
    jump act1

label casino_drink:
    scene casino_bar with dissolve
    show elysia_talk at center with dissolve

    "You choose to quietly sit at the casino bar. You order the house special and sip your drink."

    $ drink_cost = renpy.random.randint(50, 200)
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
    "A gang called the Desert Kings demands payment from workers who operate in their territory. You face a choice."
    menu:
        "Do you pay the Desert Kings?"
        "Pay the fee (lose money)":
            jump desert_pay
        "Refuse":
            jump desert_refuse

label desert_pay:
    $ payment = renpy.random.randint(100, 300)
    $ update_balance(-payment)  # Deduct payment for the gang

    hide dk_angrytalk
    show dk at center
    "You hand over $[payment] to buy 'protection.' You avoid immediate conflict, but it stings financially."

    hide dk

    show elysia_talk at center with dissolve
    "Shortly after, you befriend Leena, a veteran sex worker who helps you dodge vice cops."
    hide elysia_talk
    show elysia_huh at center
    "Meanwhile, Pure Vegas intensifies raids in your area..."
    jump act1_backlash

label desert_refuse:
    "You refuse to pay, holding on to your hard-earned cash."
    hide dk_angrytalk
    show dk_angry at center
    "Unfortunately, the Desert Kings don’t like defiance. They might retaliate with violence."
    $ gang_attack = renpy.random.randint(1, 2)
    if gang_attack == 1:
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
    menu:
        "You hear about a secret activist meeting for sex workers."
        "Attend the meeting":
            jump activism_meeting
        "Stay low":
            jump activism_avoid

label activism_meeting:
    hide sorren_talk
    show elysia_talk at center with dissolve
    "You meet other workers and social advocates. They support Sorren’s bill, sharing hopes for safety and fair treatment."
    jump legal_debates

label activism_avoid:
    hide sorren_talk
    show elysia_huh at center with dissolve
    "You skip the meeting, wary of attention. You stay alone with your worries."
    jump legal_debates

label legal_debates:
    show dk_angry at right with dissolve
    "Sorren’s proposal sparks fierce opposition from Pure Vegas. Meanwhile, the Desert Kings try to sabotage the bill to keep their black-market control."
    menu:
        "A City Council hearing invites public testimony."
        "Testify":
            hide dk_angry
            hide elysia_huh
            jump testify_scene
        "Remain silent":
            hide dk_angry
            hide elysia_huh
            jump silent_scene

label testify_scene:
    show elysia_umm at center
    "Nervously, you speak of the dangers you face daily. You might sway some council members."
    # Risk of Desert Kings targeting you for 'exposure'
    $ sabotage_chance = renpy.random.randint(1, 3)
    if sabotage_chance == 1:
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
    "With the new law in effect, you officially register as a sex worker. A Workers’ Cooperative forms to provide safer sites, medical access, and legal support."
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
    "The new casino manager, Raven Cross, proposes a VIP lounge for high-rollers seeking 'entertainment' and asks for your input. You also hear about a missing coworker, Ava."

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
    "Raven Cross, the manager at Majestic Spire, proposes an exclusive VIP lounge for high-rollers looking for legalized sexual services."
    menu:
        "Negotiate or rush?"
        "Negotiate worker protections":
            hide raven_talk
            show raven at center
            "You advocate fair wages and safety. Raven agrees, and your co-op respects your diplomacy."
            hide raven with dissolve
            show elysia at center with dissolve
            "You gain allies and a solid reputation, but the Desert Kings may retaliate."
            $ negotiate_chance = renpy.random.randint(1, 3)
            if negotiate_chance == 1:
                jump gameover_assault
        "Rush the deal":
            hide raven_talk
            show raven_smirk at center
            "You ignore crucial details for quick profit. Workers feel exploited; internal conflict escalates."
            hide raven_smirk with dissolve
            show elysia_umm at center with dissolve
            "If conflict goes too far, you might be blamed. In extreme chaos, you could face legal repercussions or violence from outraged coworkers."
            $ rush_chance = renpy.random.randint(1, 3)
            if rush_chance == 1:
                jump gameover_arrest
            else:
                hide elysia_umm
                show elysia_huh at center
                "You manage to escape the chaos, but your reputation suffers. You lose allies and face a backlash from the co-op."
                "Your actions lead to distrust and isolation, but you avoid immediate danger."
    
    $ payment = renpy.random.randint(200, 500)
    $ update_balance(payment)  # Update balance with payment
    hide elysia_huh
    hide elysia
    show elysia_talk
    "You earn $[payment] for your efforts."
        
    jump new_opportunities

label missing_worker:
    play music "32_City_and_the_City.mp3"
    scene alley_dark with dissolve
    show elysia_huh at center with dissolve
    show dk_angry at right with dissolve
    "A co-op member named Ava mysteriously disappeared. Rumor says the Desert Kings kidnapped her for disobeying them."
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
            "You focus on personal safety, but the co-op doubts your loyalty. You remain safe but skip heroics."
            jump new_opportunities

label new_opportunities:
    play music "431_Hotel_Noir.mp3"
    scene future_work with dissolve
    show elysia at right with dissolve
    "With legalized sex work, authorities now focus on genuine trafficking. The Desert Kings lose their foothold on forced labor or intimidation. You feel a fresh breeze of safety."
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
    play music "gunshot.mp3" noloop

    $ balance = 0  # Reset balance to zero on game over

    show elysia_cry at left with dissolve
    show dk_angry at right with dissolve

    "Violence strikes. The Desert Kings (or outraged associates) catch up with you. You can’t escape the assault."
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
