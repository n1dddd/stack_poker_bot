import Image from "next/image";

import Logo from "public/Logo.png"
import Club from "public/Club.png"
import Spade from "public/Spade.png"
import Heart from "public/Heart.png"
import Diamond from "public/Diamond.png"
export function TopNav() {
    return (
        <div className="w-4/5 flex-col self-center justify-self-center">
            <nav className="grid grid-cols-12 font-bold gap-8">
                <div className="col-span-5">
                    <Image
                        src={Logo}
                        quality={100}
                        alt={"Stack Poker Logo"}
                        placeholder="blur"
                        style={{ objectFit: "contain" }}
                    >
                    </Image>
                </div>
                <div className="col-span-7 flex items-center justify-between flex-wrap">
                    <div className="flex flex-col gap-2">
                        <Image
                            src={Club}
                            className="self-center"
                            alt="Club"
                            width={70}
                            height={70}
                            style={{ objectFit: "contain" }}
                            placeholder="blur"
                        ></Image>
                        <p className="text-4xl">Ranks</p>
                    </div>
                    <div className="flex flex-col gap-2">
                        <Image
                            src={Diamond}
                            className="self-center"
                            alt="Club"
                            width={70}
                            height={70}
                            style={{ objectFit: "contain" }}
                            placeholder="blur"
                        ></Image>
                        <p className="text-4xl">Tournaments</p>
                    </div>
                    <div className="flex flex-col gap-2">
                        <Image
                            src={Heart}
                            className="self-center"
                            alt="Club"
                            width={70}
                            height={70}
                            style={{ objectFit: "contain" }}
                            placeholder="blur"
                        ></Image>
                        <p className="text-4xl">Members</p>
                    </div>
                    <div className="flex flex-col gap-2">
                        <Image
                            src={Spade}
                            className="self-center"
                            alt="Club"
                            width={70}
                            height={70}
                            style={{ objectFit: "contain" }}
                            placeholder="blur"
                        ></Image>
                        <p className="text-4xl">About</p>
                    </div>
                </div>
            </nav>
        </div>
    )
}