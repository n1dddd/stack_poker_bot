export default function MemberDetails({ 
    params,
}: {
    params: { discordName: string };
}) {
    return (
        <h1>{params.discordName}</h1>
      )
}