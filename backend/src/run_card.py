from ShinyanCard.AzureServices.AzureBlobSync import AzureBlobSync
from ShinyanCard.CardCsvStore import CardCsvStore
from ShinyanCard.CardManager import CardManager
from ShinyanCard.Settings import settings
import vlc

from src.ShinyanCard.CardContents import ContentType
from src.ShinyanCard.CardMasterLevel import CardMasterLevel

azure_blob_sync = AzureBlobSync(settings.blob.storage_account_name, settings.blob.container_name)
card_store = CardCsvStore(azure_blob_sync, 'cards.csv', 'cards.csv')
card_manager = CardManager(card_store, azure_blob_sync)

while True:
    card_content_item = card_manager.next_card_content()
    print(card_content_item.text)
    print(card_content_item.translation)
    print(card_content_item.hiragana)

    audio_resource = next((r for r in card_content_item.resources if r.type.value == ContentType.AUDIO.value), None)
    player = vlc.MediaPlayer(audio_resource.uri)

    # Play the MP3
    player.play()
    current_card = card_manager.current_card
    print("\nChoose your mastery level:")
    exit_code = 999
    for choice in CardMasterLevel:
        print(f"{choice.value}: {choice.name}")
    print(f"{exit_code}: Exit")
    user_input = input("Enter a number corresponding to your choice: ")
    user_choice = int(user_input)
    if user_choice == exit_code:
        print("Exiting...")
    if user_choice in [choice.value for choice in CardMasterLevel]:
        choice = CardMasterLevel(user_choice)
        print(f"You chose {choice.name}")
        current_card.run(choice)
        card_manager.update(current_card)
        print("prepare for the next card ...")
    else:
        print("Invalid choice, please choose a number between 1 and 4.")

# source_path = Path(current_card.key) / 'examples.json'
# examples_data = None
# examples_content = azure_blob_sync.pull(source_path.as_posix())
# if examples_content is not None:
#     examples_data = json.loads(examples_content)
# else:
#     examples_data = generate_contents(settings.openai.api_key.get_secret_value(), current_card.name, "japanese")
#     azure_blob_sync.push(source_path.as_posix(), json.dumps(examples_data))
# 
# examples_items = examples_data['examples']
# if len(examples_items) > 1:
#     index = random.randint(0, len(examples_items) - 1)
#     example = examples_items[index]
#     audio_path = Path(current_card.key) / str(index) / 'audio.mp3'
#     audio = azure_blob_sync.pull(audio_path.as_posix())
#     if audio is None:
#         audio = generate_speech(settings.openai.api_key.get_secret_value(), example['Japanese'])
#         azure_blob_sync.push(audio_path.as_posix(), audio)
#     download_link = azure_blob_sync.get_download_link(audio_path.as_posix())
#     print(download_link)
#     print(example['English'])
#     print(example['Japanese'])
#     print(example['Hiragana'])






