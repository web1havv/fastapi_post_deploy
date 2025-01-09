from typing import Optional, List

from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session, joinedload
from starlette import status
from sqlalchemy import func

from app import schemas, models, oauth2
from app.database import get_db, engine

models.Base.metadata.create_all(bind=engine)
router = APIRouter(tags=['posts'])


@router.get("/posts",response_model=List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), Limit: int = 10,
              skip: int = 0, search: Optional[str] = ""):
    # cursor.execute('''SELECT * FROM posts ''')
    # posts=cursor.fetchall()
    posts = db.query(models.Post).options(joinedload(models.Post.owner)).filter(
        models.Post.title.contains(search)).limit(Limit).offset(skip).all()
    results = (
        db.query(
            models.Post,
            func.count(models.Vote.posts_id).label("votes")
        )
        .join(models.Vote, models.Vote.posts_id == models.Post.id, isouter=True)
        .group_by(models.Post.id)
        .filter(
        models.Post.title.contains(search)).limit(Limit).offset(skip)

        .all())







    return [{"post": post, "votes": votes} for post, votes in results]


@router.get("/my_posts")
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute('''SELECT * FROM posts ''')
    # posts=cursor.fetchall()
    posts = db.query(models.Post).filter(models.Post.owner_id == current_user.id).all()
    print(posts)

    return posts


@router.post('/posts', status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(new_post: schemas.PostCreate, db: Session = Depends(get_db),
                 current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""INSERT INTO posts (title,content,published) VALUES (%s,%s,%s) RETURNING * """, (new_post.title,new_post.content,new_post.published))
    # new_post=cursor.fetchone()
    # conn.commit()
    print(current_user.email)

    new_post = models.Post(owner_id=current_user.id, **new_post.dict())

    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    print('POST CREATED SUCCESSFULLY')

    return new_post


# @app.get('/posts/latest')
# def get_latest_post():
#     post = my_posts[len(my_posts) - 1]
#     return post


@router.get('/posts/{id}',response_model=schemas.PostOut)
def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    print(id)
    # cursor.execute("""SELECT * FROM posts WHERE ID = (%s)""",(str(id),))
    # particular_post= cursor.fetchone()
    # print(particular_post)
    # post = db.query(models.Post).filter(models.Post.id == id).first()
    result = (
        db.query(
            models.Post,
            func.count(models.Vote.posts_id).label("votes")
        )
        .join(models.Vote, models.Vote.posts_id == models.Post.id, isouter=True)
        .group_by(models.Post.id).filter(models.Post.id == id).first())

    if not result:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'invalid post,post not found')

    post, votes = result
    return {"post": post, "votes": votes}


@router.delete("/posts/{id}")
def delete_post(id: int, db: Session = Depends(get_db), user_id: int = Depends(oauth2.get_current_user)):
    # Fetch the specific post instance
    post = db.query(models.Post).filter(models.Post.id == id).first()

    # Check if the post exists
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {id} not found"
        )

    # Check if the current user is authorized to delete this post
    if post.owner_id != user_id.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this post"
        )

    # Delete the post
    db.delete(post)
    db.commit()

    return {"message": "Post deleted successfully"}


@router.put('/posts/{id:int}')
def update_post(id: int, post: schemas.PostUpdate, db: Session = Depends(get_db),
                user_id: int = Depends(oauth2.get_current_user)

                ):
    # index=find_index_posts(id)
    # if index is None:
    #     raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=f'invalid post,post not found')
    # post_dict=post.model_dump()
    # post_dict['id']=id
    # my_posts[index]=post_dict
    # cursor.execute('''UPDATE posts SET title=%s,content=%s,published=%s WHERE id=%s RETURNING *''',(post.title,post.content,post.published,(str(id),)))
    # updated_post=cursor.fetchone()
    # conn.commit()
    # Fetch the post from the database
    post_query = db.query(models.Post).filter(models.Post.id == id)
    first_post = post_query.first()

    # Check if the post exists
    if first_post is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid post, post not found"
        )

    # Check if the current user is authorized to update this post
    if first_post.owner_id != user_id.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized"
        )

    # Update the post with data from the Pydantic model
    post_query.update(post.dict(), synchronize_session=False)
    db.commit()

    # Return the updated post
    return {"data": post_query.first()}
