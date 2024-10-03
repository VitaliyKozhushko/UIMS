export function transformDate(dateStr: string | undefined, timeDisplay: boolean = false): string {
    if (!dateStr) return 'дата не указана'

    const date = new Date(dateStr);

    const day = date.getDate() < 10 ? '0' + date.getDate() : date.getDate();
    const month = (date.getMonth() + 1) < 10 ? '0' + (date.getMonth() + 1) : (date.getMonth() + 1);
    const year = date.getFullYear();

    let result = `${day}.${month}.${year}`;

    if (timeDisplay) {
        const hours = date.getHours() < 10 ? '0' + date.getHours() : date.getHours();
        const minutes = date.getMinutes() < 10 ? '0' + date.getMinutes() : date.getMinutes();
        result += ` ${hours}:${minutes}`;
    }

    return result
}