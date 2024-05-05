import Image from "next/image";
import Table from 'public/Table.png'
import convertToSimpleTime from "~/helper";

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
                <div key={tournament.id} className="flex md:flex-row flex-col bg-zinc-900 rounded-md w-4/5 p-8 gap-8 justify-evenly">
                    <div className="flex flex-col gap-4">
                        <div className="flex flex-col gap-4">
                            <h1 className="md:text-3xl text-2xl flex self-center font-bold">Participants</h1>
                        </div>
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
                        <div className="flex flex-row self-center flex-wrap justify-evenly gap-2">
                            {tournament.participants.map((participant: ParticipantsInfo) => (
                                <div key={participant.id} className="flex flex-wrap text-md justify-center">
                                    <span className="flex items-end">@{participant.username}</span>
                                </div>
                            ))}
                        </div>
                    </div>
                    <div className="flex flex-col gap-4 items-center justify-evenly">
                        <div className="flex flex-row gap-2">
                            <h1 className="md:text-3xl text-xl font-bold">When:</h1>
                            <h1 className="md:text-2xl text-lg self-end">{convertToSimpleTime(tournament.start_time)}</h1>
                        </div>
                        <div className="flex flex-row gap-2">
                            <h1 className="md:text-3xl text-xl font-bold">Stake:</h1>
                            <h1 className="md:text-2xl text-lg self-end">${tournament.stake}</h1>
                        </div>
                        <div className="flex flex-row gap-2">
                            <h1 className="md:text-3xl text-xl font-bold">Payout:</h1>
                            <h1 className="md:text-2xl text-lg self-end">${tournament.payout}</h1>
                        </div>
                    </div>
                </div>
            ))}
        </div>
    )

}