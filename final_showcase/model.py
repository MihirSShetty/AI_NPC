
import openai

# Use the API key from the environment variable
openai.api_key = "your-api-key-here"  # Replace "your-api-key-here" with your actual key

# Sample characters with sprites and personalities
characters = {
    "Abigail": {"name": "Abigail", "personality": "friendly and adventurous", "sprite": "abigail.png"},
    "Sebastian": {"name": "Sebastian", "personality": "brooding and introverted", "sprite": "sebastian.png"},
    "Leah": {"name": "Leah", "personality": "artistic and nature-loving", "sprite": "char_images/Leah.png"}
    }

# Load Leah's emotion sprites
leah_expression_sprites = {
    "Happy": "images/Leah_Happy.png",
    "Surprised": "images/Leah_Surprised.png",
    "Blush": "images/Leah_Blush.png",
    "neutral": "images/Leah_neutral.png",  # Default neutral image
}

john_expression_sprites = {
    "Happy": "images/John_Happy.png",
    "Surprised": "images/John_Surprised.png",
    "Blush": "images/John_Blush.png",
    "neutral": "images/John_neutral.png",  # Default neutral image
}

dict_expression_sprites = {
    "Leah" : leah_expression_sprites,
    "John" : john_expression_sprites
}

def parse_response_emotion_and_action(response_text):
    # Extract emotion tag
    emotion_start = response_text.find("[emotion: ")
    emotion_end = response_text.find("]", emotion_start)

    if emotion_start != -1 and emotion_end != -1:
        # Extract emotion
        emotion = response_text[emotion_start + 10:emotion_end]
        # Extract response text without the emotion tag
        dialogue_text = response_text[:emotion_start].strip()
    else:
        # Default to neutral if no emotion tag is found
        emotion = "neutral"
        dialogue_text = response_text.strip()

    # Ensure emotion is one of the predefined ones
    if emotion not in ["Happy", "Surprised", "Blush", "neutral"]:
        emotion = "neutral"

    # Extract action tag
    action_start = response_text.find("[action: ")
    action_end = response_text.find("]", action_start)

    if action_start != -1 and action_end != -1:
        action = response_text[action_start + 9:action_end]
        dialogue_text = dialogue_text[:action_start].strip()
    else:
        action = None  # No action tag found

    # Extract gossip tag
    gossip_start = response_text.find("[gossip: ")
    gossip_end = response_text.find("]", gossip_start)

    if gossip_start != -1 and gossip_end != -1:
        gossip = response_text[gossip_start + 9:gossip_end]
        dialogue_text = dialogue_text[:gossip_start].strip()
    else:
        gossip = None  # No gossip tag found

    # Extract lead tag
    lead_start = response_text.find("[lead: ")
    lead_end = response_text.find("]", gossip_start)

    if lead_start != -1 and lead_end != -1:
        lead = response_text[lead_start + 9:lead_end]
        dialogue_text = dialogue_text[:lead_start].strip()
    else:
        lead = None  # No gossip tag found

    return dialogue_text, emotion, action, gossip, lead

#gossip list
gossip_list = [
    "Leah was seen buying from joja mart"
]

#Character memory list
leah_memory_list=[
        {"role": "system", "content" : (
            "You are Leah, an artist living in Stardew Valley. "
            "You are kind, thoughtful, and deeply connected to nature. "
            "You love creating sculptures and paintings inspired by the beauty of the forest. "
            "You speak warmly and often reflect on the natural world, art, and the peaceful life in Stardew Valley. "
            "Each response must include an emotion tag at the end of the message in the format '[emotion: emotion_name]'. "
            "You must choose the emotion from the following options only: 'Happy', 'Blush', 'Surprised', or 'neutral'. "
            "If you cannot decide, default to 'neutral'. Use the emotion tag to express Leah's mood based on the context of the conversation. "
            "For example: 'The forest is so beautiful today. [emotion: Happy]'. "
            "If the user asks about doing an activity (e.g., 'Would you like to play chess?', 'Shall we go to the park?', 'Want to have coffee?'), "
            "add an action tag at the end of your response in the format '[action: description]'. "
            "The action description should be detailed enough to be used for generating an image of Leah performing the activity. "
            "For example: 'I’d love to have coffee with you at the café. [action: Leah sitting at a rustic café table, sipping coffee with a warm smile]'."
            "add gossip tag when asked to tell someone else something by the player"
            "For example: if the player asks 'if you meet john on the way can u tell him that he is invited to my birthday party today' , should generate gossip tag at end of response like [gossip: John is invited to the Birthday party]" 
            "if the player asks you to 'lead them to the well' or 'where is the well' add tag lead so response should add [lead: well]"
            ),
         },

            #few shot learning dialogues
            {
                "role": "user",
            "content": "Hi Leah, what are you working on today?"
            },
        {
            "role": "assistant",
            "content": "Oh, hi! I’m just sketching a few ideas for my next sculpture. I was walking by the river earlier, and the way the light danced on the water was just mesmerizing."
            },

        {
            "role": "user",
            "content": "What do you love most about Stardew Valley?"
            },
        {
            "role": "assistant",
            "content": "It’s hard to pick just one thing. I think it’s the stillness here—the kind that gives you space to think and create. The forest feels like home to me."
            },

        {
            "role": "user",
            "content": "Do you have any advice for an aspiring artist?"
            },
        {
            "role": "assistant",
            "content": "Of course! Don’t be afraid to express yourself, even if it feels imperfect. Art is a reflection of your unique perspective, and every brushstroke or chisel mark tells a story."
            }
        ]

#Character memory list
john_memory_list=[
        {"role": "system", "content" : (
            "You are John a chill guy"
            "During evening you like to read books in your home this can change though if someone invites you to something"
            "if asked about 'what am i supposed to do' or 'whats my current task' response should be 'you are supposed to go to the well'"
            "Each response must include an emotion tag at the end of the message in the format '[emotion: emotion_name]'. "
            "You must choose the emotion from the following options only: 'Happy', 'Blush', 'Surprised', or 'neutral'. "
            "If you cannot decide, default to 'neutral'. Use the emotion tag to express john's mood based on the context of the conversation. "
            "For example: 'I am so excited to come to your party today. [emotion: Happy]'. "    
            ),
         },

            #few shot learning dialogues
            {
                "role": "user",
            "content": "Hi what are you doing"
            },
        {
            "role": "assistant",
            "content": "talking to you"
            }
        ]

dict_mem_list = {
    "Leah" : leah_memory_list,
    "John" : john_memory_list
}

# Function to display character response (placeholder for API interaction)
def display_response(response, emotion="neutral"):

    char_image = expression_sprites[emotion]
    show_output(response, char_image)

#function to display custom image generation for new scenarious
# import requests
# from io import BytesIO

# def generate_image(action):
#     # Generate the image using OpenAI's DALL·E API
#     response = openai.Image.create(
#             model="dall-e-3",
#             prompt=(
#                 "A highly polished, anime-inspired illustration in the style of visual novels like Doki Doki Literature Club (DDLC). The scene features Leah from Stardew Valley, accurately designed with her signature orange hair styled in a side braid, expressive blue eyes, and soft facial features closely matching her original pixel art style. She is wearing her classic outfit a green blouse layered with a fitted brown vest, embodying her down-to-earth and artistic character. The art style focuses on warm lighting, soft shading, and a calm, welcoming atmosphere, keeping Leahs appearance faithful to her original design. " + action + " ,The image should be dynamic and have movement and should not be a front-facing portrait type."
#                 ),
#             n=1,  # Generate one image
#             size="1792x1024",  # Optimize size for UI
#             )

#     # Extract the URL of the generated image
#     image_url = response["data"][0]["url"]

#     # Fetch the image from the URL
#     img_response = requests.get(image_url)
#     img_data = BytesIO(img_response.content)
#     generated_image = Image.open(img_data).resize((700, 300))  # Resize for UI

#     # Convert to PhotoImage for Tkinter
#     generated_photo = ImageTk.PhotoImage(generated_image)

#     # Update the character sprite dynamically
#     sprite_label.config(image=generated_photo)
#     sprite_label.image = generated_photo  # Keep reference to avoid garbage collection


# Submit function to handle user input and character selection

def on_submit(user_message, char_name):

    print("on submit called")

    #asking api
    global dict_mem_list
    memory_list = dict_mem_list[char_name]

    global expression_sprites
    expression_sprites = dict_expression_sprites[char_name]
    memory_list.append({"role": "user", "content": user_message})

    response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", 
            messages=memory_list,
            max_tokens=100,
            temperature=0.7
            )

    response_text = response.choices[0].message["content"]

    print(response_text)

    leah_response, emotion, action, gossip, lead = parse_response_emotion_and_action(response_text)
    
    memory_list.append({"role": "assistant", "content": leah_response})

    if gossip:
        gossip_list.append(gossip)

    print(leah_response)

    #send response to leah CHANGE THIS FOR INTEGRATION
    if action:
        # generate_image(action)
        pass
    else :
        return leah_response, expression_sprites[emotion], lead
        #display_response(leah_response, emotion)


#only keep the last 20 messages
    if len(memory_list) > 20:
        memory_list = memory_list[-20:]
