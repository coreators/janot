import { signIn, signOut, useSession } from "next-auth/react"

export default function Header() {
    const { data: session, status } = useSession()
    const loading = status === "loading"
  
    return (
      <header>
        <noscript>
          <style>{`.nojs-show { opacity: 1; top: 0; }`}</style>
        </noscript>
        <div className="h-full w-full block">
          <div
            className={`nojs-show ${
              !session && loading ? 'relative transition-all duration-200 ease-in overflow-hidden rounded-b-md p-2 m-0 bg-gray-100 -mt-8 opacity-0' : 'relative transition-all duration-200 ease-in overflow-hidden rounded-b-md p-2 m-0 bg-gray-100'
            }`}
          >
            {!session && (
              <div className="flex-row" >
                <span className="pl-2 pr-16 whitespace-nowrap overflow-hidden inherit z-10 leading-4">
                  You are not signed in
                </span>
                <a
                  href={`/api/auth/signin`}
                  className="bg-blue-700 border-blue-700 text-white no-underline py-2 px-3"
                  onClick={(e) => {
                    e.preventDefault()
                    signIn()
                  }}
                >
                  Sign in
                </a>
              </div>
            )}
            {session?.user && (
              <>
                {session.user.image && (
                  <span
                    style={{ backgroundImage: `url('${session.user.image}')` }}
                    className="rounded-full float-left h-12 w-12 bg-white bg-cover bg-no-repeat"
                  />
                )}
                <span className="flex-row justify-start items-start pt-0  whitespace-nowrap overflow-hidden inherit z-10 leading-4">
                  <small>Signed in as</small>
                  <br />
                  <strong>{session.user.email ?? session.user.name}</strong>
                </span>
                <a
                  href={`/api/auth/signout`}
                  className="float-right -mr-1 font-medium rounded-md cursor-pointer text-base leading-5 py-2 px-2 relative z-10 bg-transparent text-gray-600"
                  onClick={(e) => {
                    e.preventDefault()
                    signOut()
                  }}
                >
                  Sign out
                </a>
              </>
            )}
          </div>
        </div>
      </header>
    )
  }
