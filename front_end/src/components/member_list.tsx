import Image from "next/image";

interface MemberInfo {
    avatar_url: string,
    bankroll: number,
    username: string,
    id: number,
    tournaments_entered: number,
    tournaments_won: Array<MemberTournamentInfo>,
}

interface MemberTournamentInfo {
    id: number,
    stake: number,
    payout: number,
}
async function getUsers() {
    const response = await fetch('http://localhost:4000/api/flask/users', { cache: 'no-store' })
        .then(res => { return res.json() })
    return response;
}

export default async function MemberList() {
    const member_list = await getUsers();
    console.log(member_list)
    return (
        <div className="flex flex-row gap-8 flex-wrap justify-evenly">
            {member_list.map((member : MemberInfo) => (
                <div key={member.id} className="flex flex-col bg-zinc-900 rounded-md md:w-64 w-4/5 items-center p-8 gap-4">
                    <Image
                        src={member.avatar_url}
                        width={75}
                        height={75}
                        className="flex rounded-full drop-shadow"
                        alt="User Profile Picture"
                        style={{ objectFit: "contain" }}
                        quality={100}
                    />

                    <h1 className="text-xl">@{member.username}</h1>
                    <h1 className="text-xl">Bankroll: ${member.bankroll}</h1>
                    <h1 className="text-xl">Tournaments Won: {member.tournaments_won.length}</h1>
                </div>
            ))}
        </div>
    )

}