import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';

// Popup content is rendered as native HTML by MapLibre GL (see map.component.ts).
// This stub component exists for potential Angular CDK Portal usage in Phase 2.
@Component({
  selector: 'app-event-popup',
  standalone: true,
  imports: [CommonModule],
  template: '',
})
export class EventPopupComponent {}
