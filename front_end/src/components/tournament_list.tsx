import Image from "next/image";

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
    start_time: Date,
    participants: ParticipantsInfo,
}
interface MemberInfo {
    avatar_url: string,
    bankroll: number,
    username: string,
    id: number

}
async function getTournaments() {
    const response = await fetch('http://localhost:4000/api/flask/tournaments',  { cache: "no-store" } )
        .then(res => { return res.json() })
    return response;
}

export default async function TournamentList() {
    const tournament_list = await getTournaments();
    console.log(tournament_list)
    return (
        <div className="flex flex-row gap-8 flex-wrap justify-evenly">
            {tournament_list.map((tournament : TournamentInfo) => (
                <div key={tournament.id} className="flex flex-col bg-zinc-900 rounded-md w-4/5 p-8">
                    <h1 className="text-xl">Tournament id: {tournament.id}</h1>
                    <h1 className="text-xl">Tournament Start Time: {tournament.start_time}</h1>
                    <h1 className="text-xl">Tournament Original Stake: ${tournament.stake}</h1>
                    <h1 className="text-xl">Tournament Payout: ${tournament.payout}</h1>
                </div>
            ))}
        </div>
    )

}