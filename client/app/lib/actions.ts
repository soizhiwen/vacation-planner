'use server';

import { revalidatePath } from 'next/cache';
import { redirect } from 'next/navigation';
import { CreatePlanState } from '@/app/lib/definitions';
import { CreatePlanFormSchema } from '@/app/lib/schemas';


const apiUrl = process.env.API_URL || 'http://127.0.0.1:8000';

export async function createPlan(prevState: CreatePlanState, formData: FormData) {
    const validatedFields = CreatePlanFormSchema.safeParse({
        budget: formData.get('budget'),
        totalDays: formData.get('totalDays'),
    });

    if (!validatedFields.success) {
        return {
            errors: validatedFields.error.flatten().fieldErrors,
            message: 'Failed to create plan.',
        };
    }

    const res = await fetch(`${apiUrl}/plans/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(validatedFields.data),
    });

    if (!res.ok) return { message: 'Failed to create plan.' };

    const json = await res.json();

    revalidatePath(`/plans/${json._id}`);
    redirect(`/plans/${json._id}`);
}


export async function readPlan(id: string) {
    const res = await fetch(`${apiUrl}/plans/${id}`, { method: 'GET' });
    if (!res.ok) return undefined;
    return await res.json();
}


export async function readPlans(limit: number) {
    const res = await fetch(`${apiUrl}/plans/?limit=${limit}`, { method: 'GET' });
    if (!res.ok) throw new Error('Failed to read plans.');
    return await res.json();
}


export async function deletePlan(id: string) {
    const res = await fetch(`${apiUrl}/plans/${id}`, { method: 'DELETE' });
    if (!res.ok) throw new Error('Failed to delete plan.');
    revalidatePath('/plans');
}