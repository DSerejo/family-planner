import {vi} from 'vitest'
import dotenv from 'dotenv';

dotenv.config(
    {
        path: '.env.test'
    }
);
vi.mock('$env/dynamic/private', () => import.meta.env);