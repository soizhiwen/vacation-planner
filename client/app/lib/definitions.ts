export type CreatePlanState = {
    errors?: {
        budget?: string[];
        totalDays?: string[];
    };
    message?: string | null;
};

export type Activity = {
    time: string;
    place: string;
    activity: string;
    notes: string;
};

export type Day = {
    day: number;
    activities: Activity[];
};

export type Plan = {
    _id: string;
    title: string;
    description: string;
    budget: number;
    totalDays: number;
    days: Day[];
    timestamp: string;
};

export type PlanWithHeader = {
    _id: string;
    title: string;
    description: string;
};

export type Plans = Plan[];