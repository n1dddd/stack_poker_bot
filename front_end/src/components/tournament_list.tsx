import Image from "next/image";
import Table from 'public/Table.png'

interface ParticipantsInfo {
    id: string,
    username: string,
    bankroll: number,
    avatar_url: string,
    rebuy_amt: number
}

interface TournamentInfo {
    id: number,
    stake: number,
    payout: number,
    start_time: any,
    participants: ParticipantsInfo,
}
interface MemberInfo {
    avatar_url: string,
    bankroll: number,
    username: string,
    id: number

}

function convertToSimpleTime(gmtTime) {
    const date = new Date(gmtTime);
    // Convert to EST time zone
    const estTime = new Date(date.toLocaleString("en-US", { timeZone: "America/New_York" }));
    // Get the components of the date
    const months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'];
    const month = months[estTime.getMonth()];
    const day = estTime.getDate();
    const hours = estTime.getHours() > 12 ? estTime.getHours() - 12 : estTime.getHours(); // Convert to 12-hour format
    const minutes = estTime.getMinutes();
    const ampm = estTime.getHours() >= 12 ? 'PM' : 'AM'; // Get AM/PM
    // Format the time components
    const formattedTime = `${month} ${day} ${hours}:${minutes < 10 ? '0' : ''}${minutes} ${ampm}`;
    return formattedTime;
}

async function getTournaments() {
    const response = await fetch('http://localhost:4000/api/flask/tournaments', { cache: "no-store" })
        .then(res => { return res.json() })
    return response;
}

export default async function TournamentList() {
    const tournament_list = await getTournaments();

    return (
        <div className="flex flex-row gap-8 flex-wrap justify-evenly">
            {tournament_list.map((tournament: TournamentInfo) => (
                <div key={tournament.id} className="flex md:flex-row flex-col bg-zinc-900 rounded-md w-4/5 p-8 gap-16 justify-evenly">
                    <Image
                        src={Table}
                        quality={100}
                        alt={"Stack Poker Logo"}
                        className="self-center flex"
                        width={300}
                        height={300}
                        style={{ objectFit: "contain" }}
                        priority
                    />
                    <div className="flex flex-col gap-8 items-center">
                        <div className="flex flex-col gap-2">
                         <h1 className="md:text-4xl text-xl">Tournament Start</h1>
                         <h1 className="md:text-2xl text-lg self-center">{convertToSimpleTime(tournament.start_time)}</h1>
                        </div>
                        <div className="flex flex-col gap-2">
                            <h1 className="md:text-4xl text-xl">Tournament Stake</h1>
                            <h1 className="md:text-2xl text-lg self-center">${tournament.stake}</h1>         
                        </div>
                        <div className="flex flex-col gap-2">
                            <h1 className="md:text-4xl text-xl">Tournament Payout</h1>
                            <h1 className="md:text-2xl text-lg self-center">${tournament.payout}</h1>         
                        </div>
                        <div className="flex flex-col gap-2">
                            <h1 className="md:text-4xl text-xl">Tournament Payout</h1>
                            <h1 className="md:text-2xl text-lg self-center">${tournament.payout}</h1>         
                        </div>
                        <div className="flex flex-col gap-2">
                            <h1 className="md:text-4xl text-2xl flex gap-4 self-center">Participants</h1>
                            <div className="flex self-center flex-wrap">
                            {tournament.participants.map((participant: ParticipantsInfo) => (
                                <div key={participant.id} className="flex flex-wrap text-md w-1/5">
                                    <span className="flex items-end">@{participant.username}</span>
                                </div>
                            ))}
                            </div>
                        </div>
                        
                    </div>
                </div>
            ))}
        </div>
    )

}