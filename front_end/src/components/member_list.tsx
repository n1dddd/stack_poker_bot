import Image from "next/image";
async function getUsers() {
    const response = await fetch('http://localhost:4000/api/flask/users', { next: { revalidate: 900 } })
        .then(res => { return res.json() })
    return response;
}

export default async function MemberList() {
    const member_list = await getUsers();
    console.log(member_list)
    return (
        <div className="flex flex-row gap-8 flex-wrap justify-evenly">
            {member_list.map((member) => (
                <div className="flex flex-col bg-zinc-900 rounded-md md:w-52 w-4/5 items-center p-8">
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

                </div>
            ))}
        </div>
    )

}