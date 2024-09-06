import OpenAI from 'openai';

const apiKey = process.env.EXPO_PUBLIC_OPENAI_API_KEY as string; // Type assertion
const openai = new OpenAI({ apiKey: apiKey, dangerouslyAllowBrowser: true });

export const createSpeechFile = async (text: string) => {
  try {
    const mp3 = await openai.audio.speech.create({
      model: "tts-1",
      voice: "alloy",
      input: text,
    });

    // Convert the ArrayBuffer to a Blob
    const arrayBuffer = await mp3.arrayBuffer();
    const blob = new Blob([arrayBuffer], { type: 'audio/mp3' });

    // Create a URL for the Blob
    const url = URL.createObjectURL(blob);

    // Create an audio element
    const audio = new Audio();
    audio.src = url;

    // Play the audio
    audio.play().then(() => {
      console.log('Speech file played successfully');
    }).catch((error) => {
      console.error('Error playing speech file:', error);
    });

  } catch (error) {
    console.error('Error creating speech file:', error);
  }
};
