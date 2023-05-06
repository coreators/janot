import Head from "next/head";
import Donut from "../components/Donut";

export default function Home() {
  return (
    <div className="flex min-h-screen flex-col items-center justify-center py-2 ">
      <Head>
        <title>JANOT</title>
      </Head>

      <main className="mx-auto w-auto px-4 pt-16 pb-8 sm:pt-24 lg:px-8">
        <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2">
          <Donut />
        </div>
        <h1 className="mt-20 mx-auto text-center text-2xl font-extrabold tracking-tight text-white sm:text-3xl lg:text-4xl xl:text-4xl">
          OS JANOT
        </h1>
      </main>
    </div>
  );
}
