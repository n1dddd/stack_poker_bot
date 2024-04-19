"use client"
import Image from "next/image";
import { usePathname } from "next/navigation";
import { cn } from "~/lib/utils";
import {motion} from "framer-motion"
import Logo from "public/Logo.png"
import Club from "public/Club.png"
import Spade from "public/Spade.png"
import Heart from "public/Heart.png"
import Diamond from "public/Diamond.png"
import Link from "next/link";


const assetList = [
    {
        id: 1,
        suit: Club,
        option: "Ranks",
        path: "/ranks",
        alt: "Club Suit Menu Icon",
    },
    {
        id: 2,
        suit: Spade,
        option: "Members",
        path: "/members",
        alt: "Spade Suit Menu Icon",
    },
    {
        id: 3,
        suit: Heart,
        option: "Tournaments",
        path: "/tournaments",
        alt: "Heart Suit Menu Icon",
    },
    {
        id: 4,
        suit: Diamond,
        option: "About",
        path: "/about",
        alt: "Diamond Suit Menu Icon",
    }

]
export function TopNav() {
    const pathname = usePathname();
    const MotionLink = motion(Link)
    const MotionImage = motion(Image)
    return (
        <div className="2xl:w-3/4 w-full flex-row self-center justify-self-center py-8">
            <nav className="grid grid-cols-12 gap-4">
                <div className="lg:col-span-5 col-span-12">
                    <Link href={"/"}>
                        <Image
                            src={Logo}
                            quality={100}
                            alt={"Stack Poker Logo"}
                            placeholder="blur" 
                            width={1920}
                            height={1080}
                            style={{ objectFit: "contain" }}
                            priority
                        >
                        </Image>
                    </Link>
                </div>
                <div className="lg:col-span-7 col-span-12 items-center justify-between content-center px-8">
                    <ul className="flex xl:flex-row flex-col justify-between">
                        {assetList.map((asset) => (
                            <MotionLink 
                                key={asset.id} 
                                href={asset.path} 
                                className={cn("rounded-md font-bold text-3xl py-2 px-2 transition-all duration-500 ease-out hover:bg-zinc-700",
                                pathname === asset.path ? "bg-zinc-600" : null

                                )}>
                                <motion.li key={asset.id} className="flex flex-row justify-between flex-shrink">
                                    <MotionImage
                                        key={asset.id}
                                        src={asset.suit}
                                        className="self-center"
                                        width={25}
                                        alt={asset.alt}
                                        style={{ objectFit: "contain" }}
                                        placeholder="blur"
                                    ></MotionImage>
                                    <motion.span key={asset.id}>{asset.option}</motion.span>
                                </motion.li>
                            </MotionLink>
                        ))}
                    </ul>
                </div>
            </nav>
        </div>
    )
}