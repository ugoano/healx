from models import Paper


def delete_paper_index():
    Paper.delete_papers()


if __name__=="__main__":
    delete_paper_index()
