export type TrackerType = 'expense'| 'asset' | 'liability';

export interface TrackerItem{

    id: string;
    type : TrackerType;
    title: string;
    amount: number;
    category: string;
    date: Date;
}