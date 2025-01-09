from fastapi import Depends, APIRouter, status, HTTPException
from sqlalchemy.orm import Session

from .. import models, schemas, database, oauth2

router = APIRouter(
    prefix="/vote",
    tags=["vote"]

)


@router.post('/', status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, db: Session = Depends(database.get_db),
         current_user: models.User = Depends(oauth2.get_current_user)):
    vote_query = db.query(models.Vote).filter(models.Vote.posts_id == vote.post_id,
                                              models.Vote.user_id == current_user.id)
    found_vote = vote_query.first()
    post=db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'Post {vote.post_id} not found')



    if (vote.dir == 1):

        if found_vote:
                raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Liked/Vote Already")
        new_vote = models.Vote(posts_id=vote.post_id, user_id=current_user.id)
        db.add(new_vote)
        db.commit()
        return {'message': 'Vote Created'}
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vote not found/exist")
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {'message': 'Vote successfully deleted'}
