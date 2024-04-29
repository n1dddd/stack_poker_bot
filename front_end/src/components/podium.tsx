import "../styles/globals.css"
import Gold from "public/Gold.png"
import Silver from "public/Silver.png"
import Bronze from "public/Bronze.png"
import Image from "next/image"

async function getUsers() {
    const response = await fetch('http://localhost:4000/api/flask/most_recent_tournament_with_users', { next: { revalidate: 3600 } })
        .then(res => { return res.json() })
    return response;
}


export default async function Podium() {
    const most_recent_tournament = await getUsers();
    const assetList = [
        {
            id: 3,
            source: Bronze,
            alt: "Stack Poker Club Bronze Medal",
            order: 3,
            height: "375px",
            background: `bronze`,
            user: most_recent_tournament.third,
            flavour_text: "#3"
        },
        {
            id: 1,
            source: Gold,
            alt: "Stack Poker Club Gold Medal",
            order: 1,
            height: "575px",
            background: `gold`,
            user: most_recent_tournament.first,
            flavour_text: "#1",
            payout: most_recent_tournament.payout
        },
        {
            id: 2,
            source: Silver,
            alt: "Stack Poker Club Silver Medal",
            order: 2,
            height: "475px",
            background: `silver`,
            user: most_recent_tournament.second,
            flavour_text: "#2"
        },
    ]

    console.log(most_recent_tournament);
    return (
        <div className="px-8 w-full flex-col self-center justify-self-center py-8 podium-card-color rounded-md">
            <div className="lg:flex flex-col gap-2">
                <h1 className="flex text-4xl text-stroke font-bold text-center">Most Recent Tournament Result</h1>
                <h1 className="flex text-2xl text-stroke font-bold text-center">When: {most_recent_tournament.start_time}</h1>
                <h1 className="flex text-2xl text-stroke font-bold text-center">Stake: ${most_recent_tournament.stake}</h1>
            </div>
            <div className="flex lg:flex-row flex-col justify-between pt-12">
                {assetList.map((asset) => (
                    <div key={asset.id} className="lg:w-1/3 w-full flex flex-col items-center justify-end gap-8" style={{ order: `${asset.order}` }}>
                        <Image
                            src={asset.source}
                            className="flex self-center drop-shadow pt-12"
                            width={200}
                            height={200}
                            quality={100}
                            alt={asset.alt}
                            style={{ objectFit: "contain" }}
                        />
                        <div className={`flex flex-col rounded-md podium-card-gradient opacity-90 ${asset.background} drop-shadow`} style={{ display: "flex", width: '300px', height: `${asset.height}` }}>
                            <div className="w-full h-full flex flex-col items-center py-8">
                                <Image
                                    src={asset.user.avatar_url}
                                    width={100}
                                    height={100}
                                    className="flex rounded-full drop-shadow"
                                    alt="User Profile Picture"
                                    style={{ objectFit: "contain" }}
                                    quality={100}
                                />
                                <div className="flex h-full flex-col items-center justify-between pt-8">
                                    <p className="flex text-3xl text-stroke font-bold text-center">@{asset.user.discord_name}</p>
                                    {asset.payout ? (<p className="flex text-3xl text-stroke font-bold text-center py-8">Payout: ${asset.payout}</p>) : (<p className="flex text-3xl text-stroke font-bold text-center py-4">Better luck next time!</p>)}
                                </div>
                            </div>
                        </div>
                    </div>
                ))}
            </div>
        </div>
    )
}