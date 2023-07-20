import { NextPage } from 'next';
import Head from 'next/head';
import React from 'react';

const Home: NextPage = () => {
  return (
    <div className="h-screen bg-black flex items-center justify-center">
      <Head>
        <title>Home</title>
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <main className="flex items-center justify-center flex-col">
        <h1 className="text-6xl text-white font-bold">
          JANOT
        </h1>
      </main>
    </div>
  );
};

export default Home;
