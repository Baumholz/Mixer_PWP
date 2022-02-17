# Diary: Hardware Group Winter Term 21/22

**Step 1: Ideation Phase** _(about 1 week)_

- Get to know each other
- Finding possible problems and use cases for WoT
- Brainstorming project ideas
- Documenting the ideas
- Presenting the ideas
- Deciding on a product/solution (dispenser/mixer)
- Separating in subteams and communicating with other groups
- Ordering hardware

**Step 2: Implementation Phase** _(about 2 weeks)_

Subteam Mixer:

- Testing the different sensors, rotation switch and socket adapter
- Writing the first code
- Dropping the vibration sensor and socket adapter
- Deciding on using switching contact for On/Off
- Ordering new rotation switch
- Testing the new rotation switch
- Soldering, gluing and building the mixer hardware
- Creating Thing Description for device
- Implementing switch and modes code
- Making UI for the AP mode
- Bug fixing (Switching between AP and other modes)

Subteam Dispenser:

- Setting up the esp and writing small code snippets for parts of the dispenser logic
  - MQTT in micropython
  - Switchbot API in micropython
  - Servo Motor in micropython → later implemented in arduino on a separate esp01
- Creating Thing Description for device
- 4-step switch setup → proved to be unreliable, replaced with rotary encoder
- Fixing mode switch for new rotary using asynchronous tasks
- Getting esp to work with low power bluetooth devices
- Re-writing switchbot python library in micropython
- Designing dispenser in cad software
- 3d printing and assembling dispenser
- Soldering/wiring esp with sensors and other hardware
- Dealing with broken hardware scheduling team coordination
- Thinking about possible solutions to provide the bluetooth api in offline mode
- Bug fixing (Switching between AP and other modes in async)
- Huge communication between all groups

**Step 3: Final Phase** _(about 1 week)_

- Tested Mixer and Dispenser hardware on the different security level
- Testing the Modes/Communication API
- Testing and combining with the other groups
- Making of the product video (planing, meeting, shooting and editing)
- Making of the presentation