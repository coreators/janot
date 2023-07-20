import { SessionProvider } from "next-auth/react"
import "../styles/globals.css";

import type { AppProps } from "next/app"
import type { Session } from "next-auth"
import { ReactElement, ReactNode } from "react";
import { NextPage } from "next";
import Layout from "../components/layout";

// eslint-disable-next-line @typescript-eslint/no-explicit-any
export type NextPageWithLayout<P = any, IP = P> = NextPage<P, IP> & {
  getLayout?: (page: ReactElement) => ReactNode;
};

type AppPropsWithLayout = AppProps<{
  session: Session;
}> & {
  Component: NextPageWithLayout;
};

// Use of the <SessionProvider> is mandatory to allow components that call
// `useSession()` anywhere in your application to access the `session` object.
export default function App({
  Component,
  pageProps: { session, ...pageProps },
}: AppPropsWithLayout) {
  const getLayout = Component.getLayout || ((page) => <Layout>{page}</Layout>);

  return (
    <SessionProvider session={session}>
      {getLayout(<Component {...pageProps} />)}
    </SessionProvider>
  )
}
