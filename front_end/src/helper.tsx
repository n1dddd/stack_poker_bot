export default function convertToSimpleTime(gmtTime) {
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
