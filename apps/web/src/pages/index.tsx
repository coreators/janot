import Head from "next/head";
import { useEffect, useRef, useState } from "react";
import CurveAnimation from "../components/CurveAnimation";
import useWhisper from "use-whisper";

import axios from "axios";

export default function Home() {
  const [ws, setWs] = useState<WebSocket>(null);
  const [isRunning, setIsRunning] = useState(false);
  const audioRef = useRef(null);


  const onTranscribe = async (blob: Blob) => {
    if (childRef.current) {
      childRef.current.run();
    }
    setIsRunning(true);
    const formdata = new FormData();
    const file = new File([blob], "speech.mp3", {
      type: "audio/mpeg",
    });
    formdata.append("audioData", file, "speech.mp3");
    formdata.append("model", "whisper-1");

    const url = `${process.env.NEXT_PUBLIC_API_SERVER_URL}/transcriptions`;
    console.log("url", url)
    const response = await axios.post(url, formdata, {
      headers: { "Content-Type": "multipart/form-data" },
    });
    const { text } = await response.data;
    // you must return result from your server in Transcript format
    if (childRef.current) {
      console.log("finish");
      childRef.current.finish();
    }

    sendMessage(text);

    return {
      blob,
      text,
    };
  };

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
      language: "ko",
    },
    // useCustomServer: true,
    onTranscribe,
    // onDataAvailable: streamToServer,
  });

  const childRef = useRef({
    listen: () => {},
    run: () => {},
    finish: () => {},
    end: () => {},
  });

  const listen = () => {
    // stt
    if (childRef.current) {
      childRef.current.listen();
    }

    startRecording();

    // start listen animation (breathing)
  };

  const run = async () => {
    // start processing animation (fast spin)
    stopRecording();
    // -> onTranscribe
  };

  useEffect(() => {
    const endpoint = `${process.env.NEXT_PUBLIC_API_SERVER_WEB_SOCKET}/chat`;
    const ws = new WebSocket(endpoint);

    ws.onmessage = async function (event) {
      const messages = document.getElementById("messages");
      const data = JSON.parse(event.data);
      if (data.sender === "bot") {
        if (data.type === "start") {
          const div = document.createElement("div");
          div.className = "server-message";
          const p = document.createElement("p");
          p.innerHTML = "JANOT: ";
          div.appendChild(p);
          messages.appendChild(div);
        } else if (data.type === "stream") {
          const p = messages.lastChild.lastChild as HTMLParagraphElement;
          if (data.message === "\n") {
            p.innerHTML += "<br>";
          } else {
            p.innerHTML += data.message;
          }
        } else if (data.type === "info") {
        } else if (data.type === "end") {
          const p = messages.lastChild.lastChild as HTMLParagraphElement;
          const finalText = (p.innerHTML).split("JANOT: ")[1];
          const enableTTS = false;
          // Call tts
          if (enableTTS) {
            const formdata = new FormData();
            formdata.append("text", finalText);
            const url = `${process.env.NEXT_PUBLIC_API_SERVER_URL}/tts`;
            const response = await axios.post(url, formdata, {
              headers: { "Content-Type": "multipart/form-data" },
              responseType: "blob",
            });
            const audioURL = URL.createObjectURL(response.data);
            const audioElement = audioRef.current;
            audioElement.src = audioURL;
            audioElement.play();
          }


          if (childRef.current) {
            console.log("end");
            childRef.current.end();
          }
          setIsRunning(false);
        } else if (data.type === "error") {
          setIsRunning(false);
          const p = messages.lastChild.lastChild as HTMLParagraphElement;
          p.innerHTML += data.message;
        }
      } else {
        const div = document.createElement("div");
        div.className = "client-message";
        const p = document.createElement("p");
        p.innerHTML = "You: ";
        p.innerHTML += data.message;
        div.appendChild(p);
        messages.appendChild(div);
      }
      // Scroll to the bottom of the chat
      messages.scrollTop = messages.scrollHeight;
    };

    setWs(ws);

    return () => {
      ws.close();
    };
  }, []);

  function sendMessage(message: string) {
    if (ws.readyState !== WebSocket.OPEN) {
      return;
    }

    if (message === "") {
      return;
    }

    ws.send(message);
  }

  return (
    <div
      className="flex min-h-screen flex-col items-center justify-center py-2 "
      onMouseDown={() => listen()}
      onTouchStart={() => listen()}
      onMouseUp={() => run()}
      onTouchEnd={() => run()}
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
          <div
            id="messages"
            className="overflow-auto text-center text-xl font-thin tracking-tight text-white"
          ></div>
        </div>
        <audio ref={audioRef} controls />
      </main>
    </div>
  );
}
