import "../styles/globals.css"
import Gold from "public/Gold.png"
import Silver from "public/Silver.png"
import Bronze from "public/Bronze.png"
import Image from "next/image"
const assetList = [
    {
        id: 2,
        source: Silver,
        alt: "Stack Poker Club Silver Medal",
        order: 2,
    },
    {
        id: 1,
        source: Gold,
        alt: "Stack Poker Club Gold Medal",
        order: 1,
    },
    {
        id: 3,
        source: Bronze,
        alt: "Stack Poker Club Bronze Medal",
        order: 3,
    }
]


async function getUsers() {
    const response = await fetch('http://localhost:4000/api/flask/most_recent_tournament_with_users', { next: { revalidate: 3600 } })
        .then(res => { return res.json() })
    return response;
}

export default async function Podium() {
    const most_recent_tournament = await getUsers();
    console.log(most_recent_tournament);
    return (
        <div className="px-8 w-full flex-col self-center justify-self-center py-8 podium-card-color rounded-md">
            <div className="lg:flex flex-col justify-between">
                <h1 className="flex text-4xl text-stroke font-bold text-center">Most Recent Tournament Result</h1>
            </div>
            <div className="flex justify-between pt-32">
                {assetList.map((asset) => (
                    <div key={asset.id} className="w-1/3 flex flex-col">
                        <Image
                            src={asset.source}
                            className="self-center drop-shadow"
                            width={200}
                            height={200}
                            quality={100}
                            alt={asset.alt}
                            style={{ objectFit: "contain" }}
                        />
                    </div>
                ))}
            </div>
        </div>
    )
}