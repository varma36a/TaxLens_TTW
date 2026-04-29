import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
    providedIn: 'root'
})
export class ApiService {
    private baseUrl = 'http://127.0.0.1:8000';

    constructor(private http: HttpClient) { }

    uploadExcel(file: File): Observable<any> {
        const formData = new FormData();
        formData.append('file', file);
        return this.http.post(`${this.baseUrl}/upload/upload-excel`, formData);
    }

    explainTax(query: string): Observable<any> {
        return this.http.post(`${this.baseUrl}/explain/tax`, { query });
    }

    compareCompanies(company1: string, company2: string): Observable<any> {
        return this.http.get(`${this.baseUrl}/compare/companies?company1=${encodeURIComponent(company1)}&company2=${encodeURIComponent(company2)}`);
    }

    getCompanyList(): Observable<any> {
        return this.http.get(`${this.baseUrl}/compare/list`);
    }

    runScenario(payload: any): Observable<any> {
        return this.http.post(`${this.baseUrl}/scenario/what-if`, payload);
    }

    getSessions(): Observable<any> {
        return this.http.get(`${this.baseUrl}/sessions/history`);
    }

    getUploads(): Observable<any> {
        return this.http.get(`${this.baseUrl}/sessions/uploads`);
    }

    getComparisons(): Observable<any> {
        return this.http.get(`${this.baseUrl}/sessions/comparisons`);
    }

    getScenarios(): Observable<any> {
        return this.http.get(`${this.baseUrl}/sessions/scenarios`);
    }
}