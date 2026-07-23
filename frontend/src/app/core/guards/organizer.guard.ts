import { inject } from '@angular/core';
import { CanActivateFn, Router } from '@angular/router';
import { AuthService } from '../services/auth.service';

/**
 * Gate the organizer console. Signed-out visitors are bounced to the auth screen
 * (remembering where they were headed); signed-in accounts without a creating
 * role are sent back to the map.
 */
export const organizerGuard: CanActivateFn = (_route, state) => {
  const auth = inject(AuthService);
  const router = inject(Router);

  if (!auth.isLoggedIn()) {
    return router.createUrlTree(['/auth'], { queryParams: { next: state.url } });
  }
  if (auth.isOrganizer()) {
    return true;
  }
  return router.createUrlTree(['/']);
};
