'use server';

import { z } from 'zod';
import { revalidatePath } from 'next/cache';
import { redirect } from 'next/navigation';

const FormSchema = z.object({
    budget: z.coerce
        .number({ message: 'Budget must be a number.' })
        .int({ message: 'Budget must be a number.' })
        .nonnegative({ message: 'Please enter an amount greater than $0.' }),
    totalDays: z.coerce
        .number({ message: 'Total days must be a number.' })
        .int({ message: 'Total days must be a number.' })
        .nonnegative({ message: 'Please enter a number greater than 0.' }),
});


export type State = {
    errors?: {
        budget?: string[];
        totalDays?: string[];
    };
    message?: string | null;
};

const apiUrl = process.env.API_URL || 'http://127.0.0.1:8000';

export async function createPlan(prevState: State, formData: FormData) {
    const validatedFields = FormSchema.safeParse({
        budget: formData.get('budget'),
        totalDays: formData.get('totalDays'),
    });

    if (!validatedFields.success) {
        return {
            errors: validatedFields.error.flatten().fieldErrors,
            message: 'Failed to create plan.',
        };
    }

    let res: Response;
    try {
        res = await fetch(`${apiUrl}/plans/`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(validatedFields.data),
        });

        if (!res.ok) {
            throw new Error('Failed to create plan.');
        }

    } catch (error) {
        return { message: 'Fetch Error: Failed to create plan.' };
    }

    const json = await res.json();

    revalidatePath(`/plans/${json._id}`);
    redirect(`/plans/${json._id}`);
}


export async function readPlan(id: string) {
    let res: Response;
    try {
        res = await fetch(`${apiUrl}/plans/${id}`, { method: 'GET' });

        if (!res.ok) {
            throw new Error('Failed to read plan.');
        }

    } catch (error) {
        return { message: 'Fetch Error: Failed to read plan.' };
    }

    return await res.json();
}


export async function readPlans(limit: number) {
    let res: Response;
    try {
        res = await fetch(`${apiUrl}/plans/?limit=${limit}`, { method: 'GET' });

        if (!res.ok) {
            throw new Error('Failed to read plans.');
        }

    } catch (error) {
        return { message: 'Fetch Error: Failed to read plans.' };
    }

    return await res.json();
}


export async function deletePlan(id: string) {
    let res: Response;
    try {
        res = await fetch(`${apiUrl}/plans/${id}`, { method: 'DELETE' });

        if (!res.ok) {
            throw new Error('Failed to delete plan.');
        }

    } catch (error) {
        return { message: 'Fetch Error: Failed to delete plan.' };
    }

    return { message: 'Deleted plan.' };
}