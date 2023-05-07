import Head from "next/head";
import Donut from "../components/Donut";

export default function Home() {

  const delay = ms => new Promise(res => setTimeout(res, ms));

  const listen = () => {
    // stt

    // start listen animation (breathing)
  }

  const process = async () => {
    // start processing animation (fast spin)
    // call chain or something

    // await processing
    // Wait 3 seconds
    await delay(3000);
    

    // start ending animation (appearing O)

    // TTS
  }



  return (
    <div className="flex min-h-screen flex-col items-center justify-center py-2 ">
      <Head>
        <title>OS-J</title>
      </Head>

      <main className="mx-auto w-auto px-4 pt-16 pb-8 sm:pt-24 lg:px-8">
        <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 z-0">
          <Donut handleListen={listen} handleProcess={process}/>
        </div>
        <h1 className="mt-24 mx-auto text-center text-2xl font-thin tracking-tight text-white sm:text-3xl lg:text-4xl xl:text-4xl">
          OS-J
        </h1>
      </main>
      {/* <div className="fixed bottom-0 w-full">
        <div className="flex flex-col items-center justify-center my-20 ">
          <button
            className="inline-flex items-center justify-center w-14 h-14 text-pink-100 transition-colors duration-150 bg-slate-50 rounded-full focus:shadow-outline hover:bg-slate-200"
            onMouseDown={() => listen()}
            onMouseUp={() => process()}
            onTouchStart={() => listen()}
            onTouchEnd={() => process()}
          >
            <svg
              fill="#000000"
              height="24"
              width="24"
              version="1.1"
              xmlns="http://www.w3.org/2000/svg"
              viewBox="0 0 512 512"
              xmlns-xlink="http://www.w3.org/1999/xlink"
              enable-background="new 0 0 512 512"
            >
              <g id="SVGRepo_bgCarrier" stroke-width="0"></g>
              <g
                id="SVGRepo_tracerCarrier"
                stroke-linecap="round"
                stroke-linejoin="round"
              ></g>
              <g id="SVGRepo_iconCarrier">
                {" "}
                <g>
                  {" "}
                  <g>
                    {" "}
                    <path d="m439.5,236c0-11.3-9.1-20.4-20.4-20.4s-20.4,9.1-20.4,20.4c0,70-64,126.9-142.7,126.9-78.7,0-142.7-56.9-142.7-126.9 0-11.3-9.1-20.4-20.4-20.4s-20.4,9.1-20.4,20.4c0,86.2 71.5,157.4 163.1,166.7v57.5h-23.6c-11.3,0-20.4,9.1-20.4,20.4 0,11.3 9.1,20.4 20.4,20.4h88c11.3,0 20.4-9.1 20.4-20.4 0-11.3-9.1-20.4-20.4-20.4h-23.6v-57.5c91.6-9.3 163.1-80.5 163.1-166.7z"></path>{" "}
                    <path d="m256,323.5c51,0 92.3-41.3 92.3-92.3v-127.9c0-51-41.3-92.3-92.3-92.3s-92.3,41.3-92.3,92.3v127.9c0,51 41.3,92.3 92.3,92.3zm-52.3-220.2c0-28.8 23.5-52.3 52.3-52.3s52.3,23.5 52.3,52.3v127.9c0,28.8-23.5,52.3-52.3,52.3s-52.3-23.5-52.3-52.3v-127.9z"></path>{" "}
                  </g>{" "}
                </g>{" "}
              </g>
            </svg>
          </button>
        </div>
      </div> */}
    </div>
  );
}
