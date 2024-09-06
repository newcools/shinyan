import React, { useState, useEffect } from 'react';
import { StyleSheet, TextInput, Button, View, SafeAreaView } from 'react-native';
import * as TaskManager from 'expo-task-manager';
import * as BackgroundFetch from 'expo-background-fetch';
import { Audio } from 'expo-av';
import { createSpeechFile } from '../openaiService';

const BACKGROUND_FETCH_TASK = 'background-fetch';

const App = () => {
  const [text, setText] = useState<string>('hello this is a test');
  const [sound, setSound] = useState<Audio.Sound | null>(null);

  useEffect(() => {
    configureBackgroundFetch();
  }, []);

  const configureBackgroundFetch = async () => {
    TaskManager.defineTask(BACKGROUND_FETCH_TASK, () => {
      try {
        console.log('Background fetch executed');
        //return BackgroundFetch.Result.NewData;
      } catch (error) {
        console.log('Background fetch failed');
        //return BackgroundFetch.Result.Failed;
      }
    });

    const status = await BackgroundFetch.getStatusAsync();
    // if (status === BackgroundFetch.Status.Available) {
    //   await BackgroundFetch.registerTaskAsync(BACKGROUND_FETCH_TASK, {
    //     minimumInterval: 15 * 60, // 15 minutes
    //     stopOnTerminate: false,
    //     startOnBoot: true,
    //   });
    // }
  };

  const playAudio = async () => {
    try {
      const fileUri = await createSpeechFile(text);
      const { sound } = await Audio.Sound.createAsync({ uri: fileUri });
      setSound(sound);
      await sound.playAsync();
    } catch (error) {
      console.error('Error playing audio:', error);
    }
  };

  const stopAudio = async () => {
    if (sound) {
      await sound.stopAsync();
      setSound(null);
    }
  };

  const startMic = () => {
    console.log('Start mic');
  };

  const stopMic = () => {
    console.log('Stop mic');
  };

  return (
    <SafeAreaView style={styles.container}>
      <TextInput
        style={styles.input}
        placeholder="Enter some text"
        value={text}
        onChangeText={setText}
      />
      <View style={styles.buttonContainer}>
        <Button title="Play Audio" onPress={playAudio} />
        <Button title="Stop Audio" onPress={stopAudio} />
        <Button title="Start Mic" onPress={startMic} />
        <Button title="Stop Mic" onPress={stopMic} />
      </View>
    </SafeAreaView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    paddingHorizontal: 16,
  },
  input: {
    height: 40,
    borderColor: 'gray',
    borderWidth: 1,
    marginBottom: 12,
    paddingHorizontal: 8,
  },
  buttonContainer: {
    flexDirection: 'column',
    justifyContent: 'space-between',
    height: 200,
  },
});

export default App;
