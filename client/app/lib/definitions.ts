export type Activity = {
    time: string;
    place: string;
    activity: string;
    notes: string;
}

export type Day = {
    day: number;
    activities: Activity[];
}

export type Plan = {
    _id: string;
    title: string;
    description: string;
    budget: number;
    totalDays: number;
    days: Day[];
    timestamp: Date;
}

export type Plans = Plan[];