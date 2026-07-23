from fastapi import APIRouter, Depends, status

from app.api.deps import get_artist_repository, get_current_user, require_role
from app.api.schemas.artist import ArtistCreate, ArtistResponse
from app.application.artists import CreateArtist, FollowArtist, GetArtist, UnfollowArtist
from app.application.dto import CreateArtistCommand
from app.application.ports import ArtistRepository
from app.domain.entities import User, UserRole

router = APIRouter(prefix="/artists", tags=["artists"])


@router.get("/{artist_id}", response_model=ArtistResponse)
async def get_artist(
    artist_id: str,
    artists: ArtistRepository = Depends(get_artist_repository),
):
    artist = await GetArtist(artists).execute(artist_id)
    return ArtistResponse.from_entity(artist)


@router.post("", response_model=ArtistResponse, status_code=status.HTTP_201_CREATED)
async def create_artist(
    body: ArtistCreate,
    current_user: User = Depends(require_role(UserRole.artist, UserRole.organizer, UserRole.admin)),
    artists: ArtistRepository = Depends(get_artist_repository),
):
    cmd = CreateArtistCommand(
        name=body.name,
        slug=body.slug,
        category=body.category,
        bio=body.bio,
        genres=body.genres,
        profile_image=body.profile_image,
        audio_preview_url=body.audio_preview_url,
        social_links=body.social_links.model_dump(exclude_none=True),
    )
    artist = await CreateArtist(artists).execute(cmd, current_user)
    return ArtistResponse.from_entity(artist)


@router.post("/{artist_id}/follow", status_code=status.HTTP_204_NO_CONTENT)
async def follow_artist(
    artist_id: str,
    current_user: User = Depends(get_current_user),
    artists: ArtistRepository = Depends(get_artist_repository),
):
    await FollowArtist(artists).execute(artist_id, current_user)


@router.delete("/{artist_id}/follow", status_code=status.HTTP_204_NO_CONTENT)
async def unfollow_artist(
    artist_id: str,
    current_user: User = Depends(get_current_user),
    artists: ArtistRepository = Depends(get_artist_repository),
):
    await UnfollowArtist(artists).execute(artist_id, current_user)
