import "../styles/globals.css"
import convertToSimpleTime from "~/helper"
import Gold from "public/Gold.png"
import Silver from "public/Silver.png"
import Bronze from "public/Bronze.png"
import Image from "next/image"

async function getMostRecentTournament() {
    try {
        const response = await fetch('http://localhost:4000/api/flask/most_recent_tournament_with_users', {cache: 'no-store' });
        const data = await response.json();
        return data;
    } catch (error) {
        console.error("Error fetching most recent tournament:", error);
        return null; // Return null if there's an error
    }
}

export default async function Podium() {
    const most_recent_tournament = await getMostRecentTournament();

    if (!most_recent_tournament) {
        return (
            <div className="px-8 w-full flex-col self-center justify-self-center py-2 rounded-md">
                <div>Nothing to show here</div>
            </div>
        )
    } else {
        const assetList = [
            {
                id: 3,
                source: Bronze,
                alt: "Stack Poker Club Bronze Medal",
                order: 1,
                height: "375px",
                background: `bronze`,
                user: most_recent_tournament.third,
                flavour_text: "Third Place"
            },
            {
                id: 1,
                source: Gold,
                alt: "Stack Poker Club Gold Medal",
                order: 2,
                height: "575px",
                background: `gold`,
                user: most_recent_tournament.first,
                flavour_text: "First Place",
                payout: most_recent_tournament.payout
            },
            {
                id: 2,
                source: Silver,
                alt: "Stack Poker Club Silver Medal",
                order: 3,
                height: "475px",
                background: `silver`,
                user: most_recent_tournament.second,
                flavour_text: "Second Place"
            },
        ];

        return (
            <div className="px-8 w-full flex-col self-center justify-self-center py-2 rounded-md bg-zinc-900 rounded-md">
                <div className="flex flex-col gap-4">
                    <h1 className="flex text-4xl text-stroke font-bold text-center">Recent Tournament Result</h1>
                    <h1 className="flex text-3xl text-stroke font-bold ">When: {convertToSimpleTime(most_recent_tournament.end_time)}</h1>
                    <h1 className="flex text-3xl text-stroke font-bold">Stake: ${most_recent_tournament.stake}</h1>
                </div>
                <div className="flex lg:flex-row flex-col justify-between pt-14">
                    {assetList.map((asset) => (
                        <div key={asset.id} className="lg:w-1/3 w-full flex flex-col items-center justify-end gap-8" style={{ order: `${asset.id}` }}>
                            <div className={`w-4/5 rounded-md flex flex-col items-center py-8 gap-6 glowing-component ${asset.background}`}>
                                <h1 className="flex text-4xl text-stroke font-bold text-center">{asset.flavour_text}</h1>
                                {asset.user && (
                                    <Image
                                        src={asset.user.avatar_url}
                                        width={125}
                                        height={125}
                                        className="flex rounded-full drop-shadow"
                                        alt="User Profile Picture"
                                        style={{ objectFit: "contain" }}
                                        quality={100}
                                    />
                                )}
                                <div className="flex flex-col items-center">
                                    {asset.user && (
                                        <p className="flex text-3xl text-stroke font-bold text-center">@{asset.user.discord_name}</p>
                                    )}
                                    {asset.payout && (
                                        <p className="flex text-2xl text-stroke font-bold text-center py-8">Payout: ${asset.payout}</p>
                                    )}                               
                                </div>
                            </div>
                            <Image
                                src={asset.source}
                                className="flex self-center drop-shadow pt-12"
                                width={400}
                                height={700}
                                quality={100}
                                alt={asset.alt}
                                style={{ objectFit: "contain" }}
                            />
                        </div>
                    ))}
                </div>
            </div>
        );
    }
}