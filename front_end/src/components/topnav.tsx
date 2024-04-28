"use client"
import React from "react";
import Image from "next/image";
import { usePathname } from "next/navigation";
import { cn } from "~/lib/utils";
import { motion } from "framer-motion"
import { Button } from "./ui/button";
import { Collapsible, CollapsibleContent, CollapsibleTrigger } from "./ui/collapsible"
import { CaretSortIcon } from "@radix-ui/react-icons"
import Logo from "public/Logo.png"
import Club from "public/Club.png"
import Spade from "public/Spade.png"
import Heart from "public/Heart.png"
import Diamond from "public/Diamond.png"
import Link from "next/link";
import "../styles/globals.css"


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
    const [isOpen, setIsOpen] = React.useState(false)
    return (
        <div className="2xl:w-3/4 xl:px-0 px-4 w-full flex-row self-center justify-self-center py-8">
            <nav className="grid grid-cols-12 gap-4">
                <div className="lg:col-span-5 col-span-12">
                    <Link href={"/"}>
                        <Image
                            src={Logo}
                            quality={100}
                            alt={"Stack Poker Logo"}
                            width={1920}
                            height={1080}
                            style={{ objectFit: "contain" }}
                            priority
                        >
                        </Image>
                    </Link>
                </div>
                <div className="lg:col-span-7 col-span-12 items-center justify-between content-center px-8">
                    <ul className="lg:flex xl:flex-row flex-col justify-between hidden">
                        {assetList.map((asset) => (
                                <MotionLink
                                    key={asset.id}
                                    href={asset.path}
                                    className={cn("rounded-md font-bold text-2xl p-4 my-1 transition-all duration-500 ease-out radial-gradient",
                                        pathname === asset.path ? "border-2 border-white" : null

                                    )}
                                    initial={{ "--x": "100%"} as any}
                                    animate={{ "--x": "-100%"} as any}
                                    whileHover={{scale: 1.1}}
                                    transition={{
                                        repeat: Infinity,
                                        repeatType: "loop",
                                        repeatDelay: 1 ,
                                        type: "spring",
                                        stiffness: 20,
                                        damping: 20,
                                        mass: 2,
                                        scale: {
                                            type: "spring",
                                            stiffness: 10,
                                            damping: 5,
                                            mass: 0.1
                                        }
                                    }}
                                    >
                                    <motion.li 
                                        className="flex flex-row gap-4 justify-between linear-mask drop-shadow-[0_1.2px_1.2px_rgba(0,0,0,0.8)]"
                                        
                                        >
                                        <MotionImage
                                            src={asset.suit}
                                            className="self-center"
                                            width={25}
                                            height={25}
                                            alt={asset.alt}
                                            style={{ objectFit: "contain" }}
                                        ></MotionImage>
                                        <motion.span 
                                        className=""
                                        >{asset.option}</motion.span>
                                    </motion.li>
                                </MotionLink>
                        ))}
                    </ul>
                </div>
                <div className="col-span-12 items-center content-center px-8">
                    <ul className="flex md:flex-col w-full">
                        <Collapsible
                            open={isOpen}
                            onOpenChange={setIsOpen}
                            className="lg:hidden lg:flex w-full"
                        >
                            <CollapsibleTrigger asChild className="flex flex-row justify-between">
                                <Button variant="secondary" className="w-full mt-2">
                                    <CaretSortIcon className="flex" />
                                    <span className="flex">Nav</span>
                                </Button>
                            </CollapsibleTrigger>
                            <CollapsibleContent className="flex-col">
                                {assetList.map((asset) => (
                                    <MotionLink
                                        key={asset.id}
                                        href={asset.path}
                                        className={cn("flex rounded-md font-bold text-2xl p-4 my-4 transition-all duration-500 ease-out radial-gradient",
                                            pathname === asset.path ? "border-2 border-white" : null
                                        )}
                                        initial={{ "--x": "100%"} as any}
                                        animate={{ "--x": "-100%"} as any}
                                        whileTap={{scale: 0.97}}
                                        transition={{
                                            repeat: Infinity,
                                            repeatType: "loop",
                                            repeatDelay: 1 ,
                                            type: "spring",
                                            stiffness: 20,
                                            damping: 20,
                                            mass: 2,
                                            scale: {
                                                type: "spring",
                                                stiffness: 10,
                                                damping: 5,
                                                mass: 0.1
                                            }
                                        }}
                                        >
                                        <motion.li key={asset.id} className="flex w-full justify-between linear-mask drop-shadow-[0_1.2px_1.2px_rgba(0,0,0,0.8)]">
                                            <MotionImage
                                                src={asset.suit}
                                                width={25}
                                                height={25}
                                                alt={asset.alt}
                                                style={{ objectFit: "contain" }}
                                            ></MotionImage>
                                            <motion.span>{asset.option}</motion.span>
                                        </motion.li>
                                    </MotionLink>
                                ))}
                            </CollapsibleContent>
                        </Collapsible>
                    </ul>
                </div>
            </nav>
        </div>
    )
}

