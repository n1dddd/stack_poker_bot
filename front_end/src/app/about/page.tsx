import Image from "next/image"
import PokerTableArt from "public/PokerTable.webp"
export default function About() {
    return (
        <section className="flex flex-col flex-wrap bg-zinc-900 rounded-md">
            <div className="flex lg:flex-row flex-col items-center">
                <Image
                    src={PokerTableArt}
                    quality={100}
                    alt={"Stack Poker Logo"}
                    className="flex rounded-md m-8"
                    width={350}
                    height={350}
                    style={{ objectFit: "contain" }}
                    priority
                />
                <h1 className="flex lg:text-2xl text-xl p-4">
                    Welcome to Stack Poker Bot Club, where our passion for poker and community come together.
                    Our Discord community hosts exciting poker nights using play chips, and we've all developed
                    a deep appreciation for the strategic and competitive aspects of the game. Poker, with its
                    blend of deception, odds-chasing, and skillful play, has become a beloved sport among our members.
                    Recognizing the need for a more efficient way to manage our fictional poker books, I embarked on
                    a journey to create a solution. The result is the Stack Poker Bot, powered by a Next.js
                    frontend, a Python microservice Discord bot, and a Flask API that ensures data persistence across
                    all user access points. The system efficiently handles user data, tournament details, results,
                    and participants, providing a robust discord-based platform for our poker nights.
                </h1>
            </div>
            <div className="flex lg:flex-row flex-col items-center">
                <h1 className=" flex lg:text-2xl text-xl lg:p-8 p-4">
                    Developing the Discord bot and integrating it with a Flask Postgres backend was a lot of fun.
                    However, I faced another obstacle: creating appealing and cohesive assets for our community. Our group,
                    a lively mix of long-time friends and newer acquaintances, has a shared history of playing a video game
                    that featured a unique and dopamine-inducing asset. It perfectly encapsulates the excitement and nostalgia
                    we feel during our poker nights. Follow our story at Stack Poker Club, where the game of poker meets innovative
                    technology and a tight-knit community. We chase the odds and play our best hands together!
                </h1>
            </div>
        </section>
    )
}