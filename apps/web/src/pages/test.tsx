import Head from "next/head";
import { useEffect, useState } from "react";
export default function TestPage() {
  const [inputText, setInputText] = useState<string>("");
  const [buttonLabel, setButtonLabel] = useState<string>("Send");
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [ws , setWs] = useState<WebSocket>(null)

  useEffect(() => {
    const endpoint = "ws://localhost:9000/chat";
    const ws = new WebSocket(endpoint);

    ws.onmessage = function (event) {
      const messages = document.getElementById("messages");
      const data = JSON.parse(event.data);
      if (data.sender === "bot") {
        if (data.type === "start") {
          const div = document.createElement("div");
          div.className = "server-message";
          const p = document.createElement("p");
          p.innerHTML = "<strong>" + "Chatbot: " + "</strong>";
          div.appendChild(p);
          messages.appendChild(div);
        } else if (data.type === "stream") {
          const header = document.getElementById("header");
          header.innerHTML = "Chatbot is typing...";
          const p = messages.lastChild.lastChild as HTMLParagraphElement;
          if (data.message === "\n") {
            p.innerHTML += "<br>";
          } else {
            p.innerHTML += data.message;
          }
        } else if (data.type === "info") {
          const header = document.getElementById("header");
          header.innerHTML = data.message;
        } else if (data.type === "end") {
          const header = document.getElementById("header");
          header.innerHTML = "Ask a question";
          setButtonLabel("Send");
          setIsLoading(false)
        } else if (data.type === "error") {
          const header = document.getElementById("header");
          header.innerHTML = "Ask a question";
          setButtonLabel("Send");
          setIsLoading(false)
          const p = messages.lastChild.lastChild as HTMLParagraphElement;
          p.innerHTML += data.message;
        }
      } else {
        const div = document.createElement("div");
        div.className = "client-message";
        const p = document.createElement("p");
        p.innerHTML = "<strong>" + "You: " + "</strong>";
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
    }
  }, [])

  function sendMessage(event: React.MouseEvent<HTMLButtonElement>) {
    event.preventDefault();

    if (ws.readyState !== WebSocket.OPEN) {
      return;
    }

    if (inputText === "") {
      return;
    }

    ws.send(inputText);
    setInputText("");

    // Turn the button into a loading button
    setButtonLabel("Loading...");
  }

  return (
    <div className="flex min-h-screen flex-col items-center justify-center py-2 ">
      <Head>
        <title>OS-J</title>
      </Head>

      <main className="mx-auto w-auto px-4 pt-16 pb-8 sm:pt-24 lg:px-8">
        <h1 className="mt-24 mx-auto text-center text-2xl font-thin tracking-tight text-white sm:text-3xl lg:text-4xl xl:text-4xl">
          OS-J
        </h1>
        <p className="card-text text-center text-sm text-white" id="header">
          Ask a question
        </p>
        <div className="flex flex-row items-end justify-end mt-4">
          <div className="mr-4">
            <input
              type="text"
              id="default-input"
              className="bg-gray-50 border border-gray-300 text-gray-800 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
              onChange={(event) => setInputText(event.target.value)}
              value={inputText}
            />
          </div>
          <button
            className="bg-gray-500 hover:bg-gray-800 text-white font-bold py-2 px-4 rounded mt-2"
            onClick={sendMessage}
            disabled={isLoading}
          >
            {buttonLabel}
          </button>
        </div>
        <div id="messages" className="overflow-auto text-white"></div>
      </main>
    </div>
  );
}
