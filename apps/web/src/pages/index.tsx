import Head from "next/head";
import { useEffect, useRef } from "react";
import CurveAnimation from "../components/CurveAnimation";
import useWhisper from "@chengsokdara/use-whisper";

import { useAudioRecorder } from 'react-audio-voice-recorder';
import axios from "axios";

export default function Home() {

  const onTranscribe = async (blob: Blob) => {
    const formdata = new FormData();
    const file = new File([blob], "speech.mp3", {
      type: "audio/mpeg",
    });
    formdata.append("audioData", file, "speech.mp3");
    formdata.append("model", "whisper-1");

    const url = "http://localhost:9000/transcriptions";
    const response = await axios.post(url, formdata, {
      headers: { "Content-Type": "multipart/form-data" },
    });
    const { text } = await response.data
    // you must return result from your server in Transcript format
    return {
      blob,
      text,
    }
  }

  const streamToServer = async (blob) => {
    const formdata = new FormData();
    const file = new File([blob], "speech.mp3", {
      type: "audio/mpeg",
    });
    formdata.append("audioData", file, "speech.mp3");
    formdata.append("model", "whisper-1");

    const url = "http://localhost:9000/transcriptions";
    const response = await axios.post(url, formdata, {
      headers: { "Content-Type": "multipart/form-data" },
    });
    const { text } = await response.data
    // you must return result from your server in Transcript format
    return {
      blob,
      text,
    }
  }

  const {
    recording,
    speaking,
    transcribing,
    transcript,
    pauseRecording,
    startRecording,
    stopRecording,
  } = useWhisper({
    // streaming: true,
    whisperConfig: {
      language: "ko"
    },
    // useCustomServer: true,
    onTranscribe,
    // onDataAvailable: streamToServer,
  })

  const childRef = useRef({
    start: () => {},
    end: () => {},
  });

  const delay = (ms: number) => new Promise((res) => setTimeout(res, ms));

  const listen = () => {
    // stt
    if (childRef.current) {
      console.log("start")
      childRef.current.start();
    }

    startRecording();

    // start listen animation (breathing)
  };

  const process = async () => {
    // start processing animation (fast spin)
    if (childRef.current) {
      childRef.current.end();
      console.log("end")
    }

    stopRecording();
    // call chain or something

    // await processing
    // Wait 3 seconds
    await delay(3000);

    // start ending animation (appearing O)

    // TTS
  };

  return (
    <div
      className="flex min-h-screen flex-col items-center justify-center py-2 "
      onMouseDown={() => listen()}
      onTouchStart={() => listen()}
      onMouseUp={() => process()}
      onTouchEnd={() => process()}
    >
      <Head>
        <title>JANOT</title>
      </Head>

      <main className="mx-auto w-auto px-4">
        <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 z-0">
          <CurveAnimation ref={childRef} />
        </div>
        <div className="flex min-h-screen flex-col items-center justify-between p-24">
          <h1 className="text-center text-2xl font-thin tracking-tight text-white sm:text-3xl lg:text-4xl xl:text-4xl">
            JANOT
          </h1>
          <p className="text-center text-2xl font-thin tracking-tight text-white">
            {transcript.text}
          </p>
        </div>
      </main>
    </div>
  );
}
