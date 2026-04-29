import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { HttpClientModule } from '@angular/common/http';
import { FormsModule } from '@angular/forms';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { ToastrModule } from 'ngx-toastr';
import { NgChartsModule } from 'ng2-charts';

import { AppComponent } from './app.component';
import { UploadWidgetComponent } from './components/upload-widget/upload-widget.component';
import { NavbarComponent } from './components/navbar/navbar.component';
import { CompareWidgetComponent } from './components/compare-widget/compare-widget.component';
import { ScenarioWidgetComponent } from './components/scenario-widget/scenario-widget.component';
import { SessionHistoryComponent } from './components/session-history/session-history.component';
import { ChatWidgetComponent } from './components/chat-widget/chat-widget.component';
import { TaxDashboardComponent } from './components/tax-dashboard/tax-dashboard.component';

@NgModule({
  declarations: [
    AppComponent,
    NavbarComponent,
    UploadWidgetComponent,
    TaxDashboardComponent,
    CompareWidgetComponent,
    ScenarioWidgetComponent,
    ChatWidgetComponent,
    SessionHistoryComponent
  ],
  imports: [
    BrowserModule,
    HttpClientModule,
    FormsModule,
    BrowserAnimationsModule,
    NgChartsModule,
    ToastrModule.forRoot()
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }