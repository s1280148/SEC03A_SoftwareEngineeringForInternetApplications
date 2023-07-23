import turbo

from BlogApp.models import Comment


class CommentStream(turbo.ModelStream):

    class Meta:
        model = Comment

    def on_save(self, comment, created, *args, **kwargs):
        if created:
            post_id = comment.post.id
            self.append("components/comment.html", {"comment": comment}, id=f"post{post_id}CommentList")
